import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from Func_H import cooling, heating_constant_curvature, loading, unloading, plot_graph
from const import *


def _plot_stress_fibers(list_t, list_sig1, list_s1, list_sig2, list_s2, title, path):
    s1o = [a + b for a, b in zip(list_sig1, list_s1)]
    s1i = [a - b for a, b in zip(list_sig1, list_s1)]
    s2i = [a + b for a, b in zip(list_sig2, list_s2)]
    s2o = [a - b for a, b in zip(list_sig2, list_s2)]
    plt.figure(figsize=(8, 5))
    plt.plot(list_t, s1o, label="layer1 outer")
    plt.plot(list_t, s1i, label="layer1 inner")
    plt.xlabel("T, K")
    plt.ylabel("Stress, Pa")
    plt.title(title + " — layer 1 (SMA)")
    plt.grid(True)
    plt.legend()
    plt.savefig(path + "_stress_layer1.png", dpi=200, bbox_inches="tight")
    plt.close()
    plt.figure(figsize=(8, 5))
    plt.plot(list_t, s2i, label="layer2 inner")
    plt.plot(list_t, s2o, label="layer2 outer")
    plt.xlabel("T, K")
    plt.ylabel("Stress, Pa")
    plt.title(title + " — layer 2 (amorphous)")
    plt.grid(True)
    plt.legend()
    plt.savefig(path + "_stress_layer2.png", dpi=200, bbox_inches="tight")
    plt.close()


def _plot_mech_stress_fibers(
    list_t,
    list_sig1_out_mech,
    list_sig1_in_mech,
    list_sig2_in_mech,
    list_sig2_out_mech,
    title,
    path,
):
    plt.figure(figsize=(8, 5))
    plt.plot(list_t, list_sig1_out_mech, label="layer1 outer (mech)")
    plt.plot(list_t, list_sig1_in_mech, label="layer1 inner (mech)")
    plt.xlabel("T, K")
    plt.ylabel("Mechanical stress, Pa")
    plt.title(title + " — mechanical stress, layer 1 (SMA)")
    plt.grid(True)
    plt.legend()
    plt.savefig(path + "_mech_stress_layer1.png", dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(list_t, list_sig2_in_mech, label="layer2 inner (mech)")
    plt.plot(list_t, list_sig2_out_mech, label="layer2 outer (mech)")
    plt.xlabel("T, K")
    plt.ylabel("Mechanical stress, Pa")
    plt.title(title + " — mechanical stress, layer 2 (amorphous)")
    plt.grid(True)
    plt.legend()
    plt.savefig(path + "_mech_stress_layer2.png", dpi=200, bbox_inches="tight")
    plt.close()


(bm, s1o, s1i, s2i, s2o, e1o, e1i, e2o, e2i, e1om, e1im, eel) = loading()
(
    s1o,
    s1i,
    s2i,
    s2o,
    sig1,
    s1,
    sig2,
    s2,
    e1ou,
    e1iu,
    e2ou,
    e2iu,
    _Mrem,
) = unloading(bm, s1o, s1i, s2i, s2o, e1o, e1i, e2o, e2i, stop_mode="sig1_out_zero")

sig1_ref, s1_ref, sig2_ref, s2_ref = sig1, s1, sig2, s2

(
    sig1,
    s1,
    sig2,
    s2,
    _fh,
    e1os,
    e1is,
    e2os,
    e2is,
    list_t,
    list_sig1,
    list_sig2,
    list_s1,
    list_s2,
    list_force,
    Fi,
    list_Fi,
    list_sig1_out_mech,
    list_sig1_in_mech,
    list_sig2_out_mech,
    list_sig2_in_mech,
) = heating_constant_curvature(
    e1ou,
    e1iu,
    e2ou,
    e2iu,
    e1om,
    e1im,
    t_start,
    t_finish,
    sig1,
    s1,
    sig2,
    s2,
    d_t=0.05,
)

f_heat = list_force

plot_graph(f_heat, list_t, "F/a (N/m)", "T, K", "Heating", show=False, save_path="out_force_heating.png")
plot_graph(list_Fi, list_t, "Fi", "T, K", "Heating Fi", show=False, save_path="out_Fi_heating.png")
_plot_stress_fibers(list_t, list_sig1, list_s1, list_sig2, list_s2, "Heating", "out_heat")
_plot_mech_stress_fibers(
    list_t,
    list_sig1_out_mech,
    list_sig1_in_mech,
    list_sig2_in_mech,
    list_sig2_out_mech,
    "Heating",
    "out_heat",
)

(
    sig1,
    s1,
    sig2,
    s2,
    _fc,
    e1os,
    e1is,
    e2os,
    e2is,
    list_tc,
    list_sig1c,
    list_sig2c,
    list_s1c,
    list_s2c,
    list_force_c,
    list_sig1_out_mech_c,
    list_sig1_in_mech_c,
    list_sig2_out_mech_c,
    list_sig2_in_mech_c,
) = cooling(
    t_finish,
    t_start,
    e1os,
    e1is,
    e2os,
    e2is,
    sig1,
    s1,
    sig2,
    s2,
    Fi,
    sig1_ref=sig1_ref,
    s1_ref=s1_ref,
    sig2_ref=sig2_ref,
    s2_ref=s2_ref,
    d_t=0.05,
)

f_cool = list_force_c

plot_graph(f_cool, list_tc, "F/a (N/m)", "T, K", "Cooling", show=False, save_path="out_force_cooling.png")
_plot_stress_fibers(list_tc, list_sig1c, list_s1c, list_sig2c, list_s2c, "Cooling", "out_cool")
_plot_mech_stress_fibers(
    list_tc,
    list_sig1_out_mech_c,
    list_sig1_in_mech_c,
    list_sig2_in_mech_c,
    list_sig2_out_mech_c,
    "Cooling",
    "out_cool",
)

plt.figure(figsize=(8, 5))
plt.plot(list_t, f_heat, label="heating")
plt.plot(list_tc, f_cool, label="cooling")
plt.xlabel("T, K")
plt.ylabel("F/a, N/m")
plt.title("Hysteresis F/a vs T")
plt.grid(True)
plt.legend()
plt.savefig("out_force_cycle.png", dpi=200, bbox_inches="tight")
plt.close()

# --- Вариант: разгрузка до нулевой кривизны (раскомментировать целиком для тех же графиков, префикс out_k0_) ---
# (bm_k, s1o_k, s1i_k, s2i_k, s2o_k, e1o_k, e1i_k, e2o_k, e2i_k, e1om_k, e1im_k, _eel_k) = loading()
# (
#     s1o_k,
#     s1i_k,
#     s2i_k,
#     s2o_k,
#     sig1_k,
#     s1_k,
#     sig2_k,
#     s2_k,
#     e1ou_k,
#     e1iu_k,
#     e2ou_k,
#     e2iu_k,
#     _Mr_k,
# ) = unloading(
#     bm_k, s1o_k, s1i_k, s2i_k, s2o_k, e1o_k, e1i_k, e2o_k, e2i_k, stop_mode="curvature_zero"
# )
# sig1_ref_k, s1_ref_k, sig2_ref_k, s2_ref_k = sig1_k, s1_k, sig2_k, s2_k
# (
#     sig1_k,
#     s1_k,
#     sig2_k,
#     s2_k,
#     _fh_k,
#     e1os_k,
#     e1is_k,
#     e2os_k,
#     e2is_k,
#     list_t_k,
#     list_sig1_k,
#     list_sig2_k,
#     list_s1_k,
#     list_s2_k,
#     list_force_k,
#     Fi_k,
#     list_Fi_k,
# ) = heating_constant_curvature(
#     e1ou_k,
#     e1iu_k,
#     e2ou_k,
#     e2iu_k,
#     e1om_k,
#     e1im_k,
#     t_start,
#     t_finish,
#     sig1_k,
#     s1_k,
#     sig2_k,
#     s2_k,
#     d_t=0.05,
# )
# f_heat_k = list_force_k
# plot_graph(
#     f_heat_k, list_t_k, "F/a (N/m)", "T, K", "Heating (curvature=0)", show=False, save_path="out_k0_force_heating.png"
# )
# plot_graph(
#     list_Fi_k, list_t_k, "Fi", "T, K", "Heating Fi (curvature=0)", show=False, save_path="out_k0_Fi_heating.png"
# )
# _plot_stress_fibers(
#     list_t_k, list_sig1_k, list_s1_k, list_sig2_k, list_s2_k, "Heating (curvature=0)", "out_k0_heat"
# )
# (
#     sig1_k,
#     s1_k,
#     sig2_k,
#     s2_k,
#     _fc_k,
#     e1os_k,
#     e1is_k,
#     e2os_k,
#     e2is_k,
#     list_tc_k,
#     list_sig1c_k,
#     list_sig2c_k,
#     list_s1c_k,
#     list_s2c_k,
#     list_force_c_k,
# ) = cooling(
#     t_finish,
#     t_start,
#     e1os_k,
#     e1is_k,
#     e2os_k,
#     e2is_k,
#     sig1_k,
#     s1_k,
#     sig2_k,
#     s2_k,
#     Fi_k,
#     sig1_ref=sig1_ref_k,
#     s1_ref=s1_ref_k,
#     sig2_ref=sig2_ref_k,
#     s2_ref=s2_ref_k,
#     d_t=0.05,
# )
# f_cool_k = list_force_c_k
# plot_graph(
#     f_cool_k, list_tc_k, "F/a (N/m)", "T, K", "Cooling (curvature=0)", show=False, save_path="out_k0_force_cooling.png"
# )
# _plot_stress_fibers(
#     list_tc_k, list_sig1c_k, list_s1c_k, list_sig2c_k, list_s2c_k, "Cooling (curvature=0)", "out_k0_cool"
# )
# plt.figure(figsize=(8, 5))
# plt.plot(list_t_k, f_heat_k, label="heating")
# plt.plot(list_tc_k, f_cool_k, label="cooling")
# plt.xlabel("T, K")
# plt.ylabel("F/a, N/m")
# plt.title("Hysteresis F/a vs T (unload curvature=0)")
# plt.grid(True)
# plt.legend()
# plt.savefig("out_k0_force_cycle.png", dpi=200, bbox_inches="tight")
# plt.close()
