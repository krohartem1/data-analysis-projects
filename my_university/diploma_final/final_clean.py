"""ФИНАЛЬНЫЙ прогон: оригинальный Func_H.py (без T·dα), L_eff=0, k_CC=0.12.
Графики F(T) и эволюции σ_out на тренировке."""
import contextlib, importlib.util, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def reset(funch, kcc):
    for mod in ['Func_H', 'const']:
        if mod in sys.modules: del sys.modules[mod]
    spec = importlib.util.spec_from_file_location('Func_H', funch)
    m = importlib.util.module_from_spec(spec); sys.modules['Func_H'] = m
    spec.loader.exec_module(m)
    spec_c = importlib.util.spec_from_file_location('const', 'const.py')
    mc = importlib.util.module_from_spec(spec_c); sys.modules['const'] = mc
    spec_c.loader.exec_module(mc)
    m.k_CC = kcc; mc.k_CC = kcc
    return m, mc

def run_full(m, mc, h1, h2, delta, L, n_train=30):
    mc.h1=h1; mc.h2=h2; mc.delta=delta; mc.part_len=L; mc.L_eff_offset=0.0
    m.h1=h1; m.h2=h2; m.delta=delta; m.part_len=L; m.L_eff_offset=0.0
    m.podat1_unload=(1/mc.strengthening_coefficient_1)-(1/mc.unloading_young_module_1)
    m.podat1_load=(1/mc.strengthening_coefficient_1)-(1/mc.loading_young_module_1)
    m.podat2=(1/mc.strengthening_coefficient_2)-(1/mc.young_module_2)
    sig1_train_history = []
    with contextlib.redirect_stdout(open(os.devnull,'w')):
        r=m.loading()
        bm,s1o,s1i,s2i,s2o,e1o,e1i,e2o,e2i,e1om,e1im,ee,sy_o,sy_i=r
        u=m.unloading(bm,s1o,s1i,s2i,s2o,e1o,e1i,e2o,e2i)
        s1o_u,s1i_u,s2i_u,s2o_u,sig1,ss1,sig2,ss2,e1ou,e1iu,e2ou,e2iu,M=u
        rt=m.free_thermal_cycle(e1ou,e1iu,e2ou,e2iu,e1om,e1im,sig1,ss1,sig2,ss2,n_cycles=n_train,d_t=1.0)
        sig1,ss1,sig2,ss2=rt['sig1'],rt['s1'],rt['sig2'],rt['s2']
        e1ou,e1iu,e2ou,e2iu=rt['eps1_out'],rt['eps1_in'],rt['eps2_out'],rt['eps2_in']
        zd=rt['zeta_d']
        for h in rt['history']:
            if 'sig1_out' in h:
                sig1_train_history.append(h['sig1_out'])
        s1r,ssr1,s2r,ssr2=sig1,ss1,sig2,ss2
        rh=m.heating_constant_curvature(e1ou,e1iu,e2ou,e2iu,e1om,e1im,
            mc.t_start,mc.t_finish,sig1,ss1,sig2,ss2,d_t=0.05,
            sig1_out_yield_signed=sy_o,sig1_in_yield_signed=sy_i,zeta_d_in=zd)
        sig1,ss1,sig2,ss2,_f,e1oh,e1ih,e2oh,e2ih,list_t_h,_,_,list_F_h,Fi_end,_=rh
        zd=m.heating_constant_curvature.last_zeta_d
        rc=m.cooling(mc.t_finish, mc.t_start, e1oh, e1ih, e2oh, e2ih,
            sig1, ss1, sig2, ss2, Fi_end,
            sig1_ref=s1r, s1_ref=ssr1, sig2_ref=s2r, s2_ref=ssr2,
            d_t=0.05, zeta_d_in=zd)
        sig1,ss1,sig2,ss2,_f,e1oc,e1ic,e2oc,e2ic,list_t_c,_,_,list_F_c=rc
    return {
        'list_t_h': list_t_h, 'list_F_h': list_F_h,
        'list_t_c': list_t_c, 'list_F_c': list_F_c,
        'F_max_h': max(list_F_h), 'F_max_c': max(list_F_c), 'F_min_c': min(list_F_c),
        'sig1_train_history': sig1_train_history,
    }

samples = {
    'АК1': {'h1': 6.86e-6,  'h2': 24.07e-6, 'delta': 600e-6,  'L': 3e-3, 'F_exp': 6.0},
    'АК2': {'h1': 8.80e-6,  'h2': 28.27e-6, 'delta': 400e-6,  'L': 3e-3, 'F_exp': 6.0},
    'АК3': {'h1': 12.19e-6, 'h2': 31.40e-6, 'delta': 700e-6,  'L': 3e-3, 'F_exp': 16.0},
}

print("ФИНАЛЬНЫЙ прогон — Func_H.py (оригинал), k_CC=0.12, L_eff=0, БЕЗ T·dα")
print("="*70)
results = {}
for name, p in samples.items():
    m, mc = reset('Func_H.py', 1.2e-7)
    res = run_full(m, mc, p['h1'], p['h2'], p['delta'], p['L'])
    results[name] = res
    err = 100*abs(res['F_max_h'] - p['F_exp'])/p['F_exp']
    print(f"  {name}: δ={p['delta']*1e6:.0f}мкм → F_max нагр={res['F_max_h']:.3f}, "
          f"F_max охл={res['F_max_c']:.3f}, F_min={res['F_min_c']:+.3f} | "
          f"эксп F={p['F_exp']:.1f} | ошибка {err:.2f}%")

# График F(T)
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
for i, (name, p) in enumerate(samples.items()):
    ax = axes[i]; res = results[name]
    ax.plot(res['list_t_h'], res['list_F_h'], 'r-', lw=2.2, label='нагрев')
    ax.plot(res['list_t_c'], res['list_F_c'], 'b-', lw=2.2, label='охлаждение')
    ax.axhline(p['F_exp'], color='black', linestyle=':', lw=2,
               label=f'эксп F_max = {p["F_exp"]:.1f} Н/м')
    ax.set_xlabel('T, K', fontsize=11)
    ax.set_ylabel('F/a, Н/м', fontsize=11)
    ax.set_title(f"{name}: h₁={1e6*p['h1']:.2f} мкм, δ={1e6*p['delta']:.0f} мкм",
                 fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3); ax.legend(fontsize=10, loc='best')
plt.suptitle('F(T) для трёх образцов — финальная модель (k_CC=0.12, L_eff=0, без T·dα)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('final_F_vs_T_clean.png', dpi=180, bbox_inches='tight')
plt.close()

# Тренировка
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
for i, (name, p) in enumerate(samples.items()):
    ax = axes[i]; res = results[name]
    cycles = list(range(1, len(res['sig1_train_history']) + 1))
    ax.plot(cycles, [s/1e6 for s in res['sig1_train_history']], 'go-', lw=1.8, ms=4)
    ax.set_xlabel('номер цикла тренировки', fontsize=11)
    ax.set_ylabel('σ_out СПФ при T = T_finish, МПа', fontsize=11)
    ax.set_title(f"{name}: тренировка (M=0)", fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3)
plt.suptitle('Эволюция σ_out СПФ-слоя на тренировке (30 свободных циклов)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('final_training_clean.png', dpi=180, bbox_inches='tight')
plt.close()

print("\nГрафики сохранены: final_F_vs_T.png, final_training.png")
