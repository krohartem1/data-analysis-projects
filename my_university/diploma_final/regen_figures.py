"""Регенерация всех графиков с Беляевскими параметрами."""
import contextlib, importlib.util, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIGS = 'figures'
os.makedirs(FIGS, exist_ok=True)

def reset(funch='Func_H.py', kcc=1.2e-7, K_r=0.66, E_TP=10e9):
    for mod in ['Func_H', 'const']:
        if mod in sys.modules: del sys.modules[mod]
    spec = importlib.util.spec_from_file_location('Func_H', funch)
    m = importlib.util.module_from_spec(spec); sys.modules['Func_H'] = m
    spec.loader.exec_module(m)
    spec_c = importlib.util.spec_from_file_location('const', 'const.py')
    mc = importlib.util.module_from_spec(spec_c); sys.modules['const'] = mc
    spec_c.loader.exec_module(mc)
    m.k_CC = kcc; mc.k_CC = kcc
    mc.rec_ratio = K_r; m.rec_ratio = K_r
    mc.young_module_TP = E_TP; m.young_module_TP = E_TP
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
    'АК1': {'h1': 6.86e-6,  'h2': 24.07e-6, 'delta': 760e-6, 'L': 3e-3, 'F_exp': 6.0},
    'АК2': {'h1': 8.80e-6,  'h2': 28.27e-6, 'delta': 550e-6, 'L': 3e-3, 'F_exp': 6.0},
    'АК3': {'h1': 12.19e-6, 'h2': 31.40e-6, 'delta': 828e-6, 'L': 3e-3, 'F_exp': 16.0},
}

# === 1) F(T) для трёх образцов ===
print("[1/5] F(T) для трёх образцов")
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
results = {}
for i, (name, p) in enumerate(samples.items()):
    m, mc = reset()
    res = run_full(m, mc, p['h1'], p['h2'], p['delta'], p['L'])
    results[name] = res
    err = 100*abs(res['F_max_h'] - p['F_exp'])/p['F_exp']
    print(f"  {name}: δ={p['delta']*1e6:.0f}мкм → F_max={res['F_max_h']:.3f}, F_min={res['F_min_c']:+.3f}, ошибка {err:.2f}%")
    ax = axes[i]
    ax.plot(res['list_t_h'], res['list_F_h'], 'r-', lw=2.2, label='нагрев')
    ax.plot(res['list_t_c'], res['list_F_c'], 'b-', lw=2.2, label='охлаждение')
    ax.axhline(p['F_exp'], color='black', linestyle=':', lw=2,
               label=f'эксп F_max = {p["F_exp"]:.1f} Н/м')
    ax.set_xlabel('T, K', fontsize=11)
    ax.set_ylabel('F/a, Н/м', fontsize=11)
    ax.set_title(f"{name}: $h_1$={1e6*p['h1']:.2f} мкм, δ={1e6*p['delta']:.0f} мкм",
                 fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3); ax.legend(fontsize=10, loc='best')
plt.suptitle('Расчётная зависимость $F(T)$ для трёх образцов\n'
             '(K_r=0,66, $E_{ПП}$=10 ГПа — значения Беляев 2015)',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGS}/final_F_vs_T.png', dpi=180, bbox_inches='tight')
plt.close()

# === 2) Эволюция σ_out СПФ слоя на тренировке ===
print("[2/5] Тренировка")
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
for i, (name, p) in enumerate(samples.items()):
    ax = axes[i]; res = results[name]
    cycles = list(range(1, len(res['sig1_train_history']) + 1))
    ax.plot(cycles, [s/1e6 for s in res['sig1_train_history']], 'go-', lw=1.8, ms=5)
    ax.set_xlabel('номер цикла тренировки', fontsize=11)
    ax.set_ylabel('$\\sigma_1^{out}$ при $T = T_f$, МПа', fontsize=11)
    ax.set_title(f"{name}: тренировка ($M=0$)", fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3)
plt.suptitle('Эволюция напряжения в наружном волокне СПФ-слоя при свободном термоциклировании (30 циклов)',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGS}/training_evolution.png', dpi=180, bbox_inches='tight')
plt.close()

# === 3) Сравнение с тренировкой и без ===
print("[3/5] С тренировкой vs без")
def run_no_train(m, mc, h1, h2, delta, L):
    mc.h1=h1; mc.h2=h2; mc.delta=delta; mc.part_len=L; mc.L_eff_offset=0.0
    m.h1=h1; m.h2=h2; m.delta=delta; m.part_len=L; m.L_eff_offset=0.0
    m.podat1_unload=(1/mc.strengthening_coefficient_1)-(1/mc.unloading_young_module_1)
    m.podat1_load=(1/mc.strengthening_coefficient_1)-(1/mc.loading_young_module_1)
    m.podat2=(1/mc.strengthening_coefficient_2)-(1/mc.young_module_2)
    with contextlib.redirect_stdout(open(os.devnull,'w')):
        r=m.loading()
        bm,s1o,s1i,s2i,s2o,e1o,e1i,e2o,e2i,e1om,e1im,ee,sy_o,sy_i=r
        u=m.unloading(bm,s1o,s1i,s2i,s2o,e1o,e1i,e2o,e2i)
        s1o_u,s1i_u,s2i_u,s2o_u,sig1,ss1,sig2,ss2,e1ou,e1iu,e2ou,e2iu,M=u
        s1r,ssr1,s2r,ssr2=sig1,ss1,sig2,ss2
        rh=m.heating_constant_curvature(e1ou,e1iu,e2ou,e2iu,e1om,e1im,
            mc.t_start,mc.t_finish,sig1,ss1,sig2,ss2,d_t=0.05,
            sig1_out_yield_signed=sy_o,sig1_in_yield_signed=sy_i,zeta_d_in=0.0)
        sig1,ss1,sig2,ss2,_f,e1oh,e1ih,e2oh,e2ih,list_t_h,_,_,list_F_h,Fi_end,_=rh
        zd=m.heating_constant_curvature.last_zeta_d
        rc=m.cooling(mc.t_finish, mc.t_start, e1oh, e1ih, e2oh, e2ih,
            sig1, ss1, sig2, ss2, Fi_end,
            sig1_ref=s1r, s1_ref=ssr1, sig2_ref=s2r, s2_ref=ssr2,
            d_t=0.05, zeta_d_in=zd)
        sig1,ss1,sig2,ss2,_f,e1oc,e1ic,e2oc,e2ic,list_t_c,_,_,list_F_c=rc
    return {'list_t_h': list_t_h, 'list_F_h': list_F_h, 
            'list_t_c': list_t_c, 'list_F_c': list_F_c,
            'F_max_h': max(list_F_h), 'F_min_c': min(list_F_c)}

fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
for i, (name, p) in enumerate(samples.items()):
    ax = axes[i]
    # Без тренировки
    m, mc = reset()
    res_nt = run_no_train(m, mc, p['h1'], p['h2'], p['delta'], p['L'])
    # С тренировкой
    res_t = results[name]
    ax.plot(res_nt['list_t_h'], res_nt['list_F_h'], 'r--', lw=1.6, label='нагрев (без трен.)')
    ax.plot(res_nt['list_t_c'], res_nt['list_F_c'], 'b--', lw=1.6, label='охлажд. (без трен.)')
    ax.plot(res_t['list_t_h'], res_t['list_F_h'], 'r-', lw=2.3, label='нагрев (30 циклов)')
    ax.plot(res_t['list_t_c'], res_t['list_F_c'], 'b-', lw=2.3, label='охлажд. (30 циклов)')
    ax.axhline(p['F_exp'], color='black', linestyle=':', lw=1.5,
               label=f'эксп F_max = {p["F_exp"]:.1f}')
    ax.set_xlabel('T, K', fontsize=11)
    ax.set_ylabel('F/a, Н/м', fontsize=11)
    ax.set_title(f"{name}", fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3); ax.legend(fontsize=9, loc='best')
plt.suptitle('Эффект тренировки: F(T) без тренировки vs после 30 свободных циклов',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGS}/training_vs_no_training_3samples.png', dpi=180, bbox_inches='tight')
plt.close()

# === 4) Валидация F_max(L) на 17 длинах × 3 образца ===
print("[4/5] Валидация на 17 длинах × 3 образца")
L_grid = np.linspace(1e-3, 5e-3, 17)
F_exp_pts = {
    'АК1': {'L': [1,2,3,4,5], 'F': [13.0, 9.0, 6.0, 5.0, 4.0]},
    'АК2': {'L': [1,2,3,4,5], 'F': [10.0, 9.0, 6.0, 5.0, 4.0]},
    'АК3': {'L': [1,2,3,4,5], 'F': [27.0, 17.0, 16.0, 12.0, 10.0]},
}

def run_max_quick(m, mc, h1, h2, delta, L):
    mc.h1=h1; mc.h2=h2; mc.delta=delta; mc.part_len=L; mc.L_eff_offset=0.0
    m.h1=h1; m.h2=h2; m.delta=delta; m.part_len=L; m.L_eff_offset=0.0
    m.podat1_unload=(1/mc.strengthening_coefficient_1)-(1/mc.unloading_young_module_1)
    m.podat1_load=(1/mc.strengthening_coefficient_1)-(1/mc.loading_young_module_1)
    m.podat2=(1/mc.strengthening_coefficient_2)-(1/mc.young_module_2)
    with contextlib.redirect_stdout(open(os.devnull,'w')):
        r=m.loading()
        bm,s1o,s1i,s2i,s2o,e1o,e1i,e2o,e2i,e1om,e1im,ee,sy_o,sy_i=r
        u=m.unloading(bm,s1o,s1i,s2i,s2o,e1o,e1i,e2o,e2i)
        s1o_u,s1i_u,s2i_u,s2o_u,sig1,ss1,sig2,ss2,e1ou,e1iu,e2ou,e2iu,M=u
        rt=m.free_thermal_cycle(e1ou,e1iu,e2ou,e2iu,e1om,e1im,sig1,ss1,sig2,ss2,n_cycles=15,d_t=1.0)
        sig1,ss1,sig2,ss2=rt['sig1'],rt['s1'],rt['sig2'],rt['s2']
        e1ou,e1iu,e2ou,e2iu=rt['eps1_out'],rt['eps1_in'],rt['eps2_out'],rt['eps2_in']
        zd=rt['zeta_d']
        rh=m.heating_constant_curvature(e1ou,e1iu,e2ou,e2iu,e1om,e1im,
            mc.t_start,mc.t_finish,sig1,ss1,sig2,ss2,d_t=0.1,
            sig1_out_yield_signed=sy_o,sig1_in_yield_signed=sy_i,zeta_d_in=zd)
        _,_,_,_,_f,_,_,_,_,_,_,_,list_F_h,_,_=rh
    return max(list_F_h)

model_results = {}
for name, p in samples.items():
    print(f"  {name}...")
    F_model = []
    for L in L_grid:
        m, mc = reset()
        F = run_max_quick(m, mc, p['h1'], p['h2'], p['delta'], L)
        F_model.append(F)
    model_results[name] = F_model

fig, axes = plt.subplots(2, 3, figsize=(16, 9), gridspec_kw={'height_ratios': [2, 1]})
for i, (name, p) in enumerate(samples.items()):
    ax = axes[0][i]
    L_mm = L_grid * 1e3
    ax.plot(L_mm, model_results[name], 'b-o', lw=2, ms=5, label='модель')
    ax.plot(F_exp_pts[name]['L'], F_exp_pts[name]['F'], 'r^', ms=11, label='эксперимент', zorder=5)
    ax.axvline(3, color='green', alpha=0.3, lw=2, label='точка калибровки (L=3 мм)')
    ax.set_xlabel('L, мм', fontsize=11)
    ax.set_ylabel('F$_{\\rm max}$/a, Н/м', fontsize=11)
    ax.set_title(f"{name}: $h_1$={p['h1']*1e6:.2f} мкм, δ={p['delta']*1e6:.0f} мкм",
                 fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3); ax.legend(fontsize=10)
    
    # Гистограмма ошибок
    ax2 = axes[1][i]
    L_exp = np.array(F_exp_pts[name]['L'])
    F_exp_v = np.array(F_exp_pts[name]['F'])
    F_mod_at_exp = np.interp(L_exp, L_mm, model_results[name])
    err = 100*(F_mod_at_exp - F_exp_v)/F_exp_v
    colors = ['green' if abs(e)<10 else ('orange' if abs(e)<25 else 'red') for e in err]
    ax2.bar(L_exp, err, color=colors, edgecolor='black')
    ax2.axhline(0, color='black', lw=0.5)
    ax2.set_xlabel('L, мм', fontsize=11)
    ax2.set_ylabel('Отклонение, %', fontsize=11)
    ax2.set_title(f"Ошибка модели по {name}", fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
plt.suptitle('Валидация модели на 17 длинах L по каждому образцу (точки — эксперимент Шелякова)',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGS}/validation_F_vs_L.png', dpi=180, bbox_inches='tight')
plt.close()

# === 5) Кинетика Φ(T) ===
print("[5/5] Кинетика Φ(T)")
m, mc = reset()
T = np.linspace(280, 360, 400)
As, Af, Ms, Mf = mc.a_start, mc.a_finish, mc.m_start, mc.m_finish
# Косинусная Лианг-Роджерс
Phi_heat = np.zeros_like(T)
Phi_cool = np.zeros_like(T)
for i, t in enumerate(T):
    if t <= As: Phi_heat[i] = 1
    elif t >= Af: Phi_heat[i] = 0
    else: Phi_heat[i] = 0.5 * (1 + np.cos(np.pi*(t-As)/(Af-As)))
    if t >= Ms: Phi_cool[i] = 0
    elif t <= Mf: Phi_cool[i] = 1
    else: Phi_cool[i] = 0.5 * (1 - np.cos(np.pi*(Ms-t)/(Ms-Mf)))

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(T, Phi_cool, 'b-', lw=2.5, label='Охлаждение (A→M)')
ax.plot(T, Phi_heat, 'r-', lw=2.5, label='Нагрев (M→A)')
ax.axvline(Mf, ls=':', alpha=0.5, color='gray')
ax.axvline(As, ls=':', alpha=0.5, color='gray')
ax.axvline(Ms, ls=':', alpha=0.5, color='gray')
ax.axvline(Af, ls=':', alpha=0.5, color='gray')
ax.text(Mf-1, -0.05, '$M_f$', ha='right', fontsize=11)
ax.text(As+1, -0.05, '$A_s$', ha='left', fontsize=11)
ax.text(Ms-1, -0.05, '$M_s$', ha='right', fontsize=11)
ax.text(Af+1, -0.05, '$A_f$', ha='left', fontsize=11)
ax.annotate('Мартенсит', xy=(295, 0.5), fontsize=12, 
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
ax.annotate('Аустенит', xy=(348, 0.5), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
ax.set_xlabel('Температура $T$, K', fontsize=12)
ax.set_ylabel('Объёмная доля мартенсита $\\Phi$', fontsize=12)
ax.set_title('Кинетика мартенситного превращения для Ti$_{50}$Ni$_{25}$Cu$_{25}$\n'
             '(косинусная аппроксимация по Liang-Rogers)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3); ax.legend(fontsize=11, loc='center right')
ax.set_xlim(280, 360); ax.set_ylim(-0.1, 1.1)
plt.tight_layout()
plt.savefig(f'{FIGS}/phi_kinetics.png', dpi=180, bbox_inches='tight')
plt.close()

print("\nВсе графики сохранены в", FIGS)
import os as o
for f in sorted(o.listdir(FIGS)):
    sz = o.path.getsize(f'{FIGS}/{f}')
    print(f"  {f}: {sz//1024} KB")
