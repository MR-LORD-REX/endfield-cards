var rl = Object.freeze
  , ka = Object.defineProperty;
var nl = (s, e) => rl(ka(s, "raw", {
    value: rl(e || s.slice())
}));
import {s as Qe, D as Oe, i as M, f as h, C as at, G as ve, c as Ia, e as b, k as H, t as De, b as k, d as E, m as R, l as Se, h as d, o as te, I as z, j as g, z as mt, J as Fe, u as Da, g as Sa, a as $a, r as ua, A as Pe, T as lt, n as be, M as ha, L as Dt, P as Ke, N as nt, H as Aa, O as Ea, y as wa, Q as ya, R as Ca, S as Xt, U as qt, V as Jt} from "./scheduler.091fad8f.js";
import {S as Ye, i as Je, c as j, b as K, m as Q, t as I, a as y, d as Y, g as me, e as de, h as Zt} from "./index.65ada347.js";
import {I as _a} from "./ZZZCard.svelte_svelte_type_style_lang.a031ccf8.js";
import {D as Pa} from "./DraggableCanvas.78bf0e30.js";
import "./alg.140d3c08.js";
import {p as Na} from "./stores.4b91e205.js";
import {k as xt, z as J, D as q, F as Va, I as Ta, J as Tt, K as ol, L as Ma} from "./LodaHoyoView.svelte_svelte_type_style_lang.481f382d.js";
import {E as Mt} from "./EfIcon.671ee85d.js";
import {w as Nt} from "./paths.367e7f08.js";
import {e as ee} from "./each.4ab6351a.js";
import {L as Ha} from "./stores.56fc16e0.js";
import {a as Ra, b as La, c as zt, d as Fa, L as Ba} from "./CardSettingsContext.1cb0e80a.js";
import {B as Ga, V as Ua, T as Wa} from "./Button.a027d1a2.js";
import {b as Oa} from "./navigation.806a946c.js";
import "./index.b28669b7.js";
import {C as qa} from "./Clientside.e70febae.js";
import {L as Vt, R as cl, g as za, h as ja} from "./canvas.9427fbb2.js";
import "./SaveNewBuildFloat.6c09c4e5.js";
/* empty css                                            */
/* empty css                                                 */
import "./Checkbox.svelte_svelte_type_style_lang.8f4722de.js";
/* empty css                                            */
import {C as Ka} from "./CanvasIcon.340c0b7a.js";
function Qa(s) {
    let e, l;
    return e = new Mt({
        props: {
            name: s[0].simpleName
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, [a]) {
            const i = {};
            a & 1 && (i.name = t[0].simpleName),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function Ya(s, e, l) {
    let {prop: t=null} = e;
    return s.$$set = a => {
        "prop"in a && l(0, t = a.prop)
    }
    ,
    [t]
}
class ma extends Ye {
    constructor(e) {
        super(),
        Je(this, e, Ya, Qa, Qe, {
            prop: 0
        })
    }
}
const Ja = s => ({})
  , fl = s => ({});
function ul(s, e, l) {
    const t = s.slice();
    return t[2] = e[l],
    t
}
function hl(s) {
    let e, l, t, a, i, r, o, n, f = s[2].formatted + "", c, u, m, A, P, p = s[7] && _l(), D = s[1] && ml(s);
    i = new ma({
        props: {
            prop: s[2]
        }
    });
    let w = s[5] && gl(s)
      , _ = s[0] && pl();
    const V = s[22].postfix
      , T = Ia(V, s, s[21], fl);
    return {
        c() {
            e = b("div"),
            p && p.c(),
            l = H(),
            t = b("figure"),
            D && D.c(),
            a = H(),
            j(i.$$.fragment),
            r = H(),
            w && w.c(),
            o = H(),
            n = b("span"),
            _ && _.c(),
            c = De(f),
            u = H(),
            T && T.c(),
            this.h()
        },
        l(N) {
            e = k(N, "DIV", {
                class: !0,
                style: !0
            });
            var G = E(e);
            p && p.l(G),
            l = R(G),
            t = k(G, "FIGURE", {
                class: !0
            });
            var ae = E(t);
            D && D.l(ae),
            a = R(ae),
            K(i.$$.fragment, ae),
            ae.forEach(h),
            r = R(G),
            w && w.l(G),
            o = R(G),
            n = k(G, "SPAN", {
                class: !0
            });
            var x = E(n);
            _ && _.l(x),
            c = Se(x, f),
            x.forEach(h),
            u = R(G),
            T && T.l(G),
            G.forEach(h),
            this.h()
        },
        h() {
            var N;
            d(t, "class", "svelte-g2rt2f"),
            d(n, "class", "efnum svelte-g2rt2f"),
            d(e, "class", "Prop svelte-g2rt2f"),
            te(e, "--extra", ((N = s[1]) == null ? void 0 : N.length) || 0),
            z(e, "primary", s[8]),
            z(e, "soft", s[4]),
            z(e, "full", s[5]),
            z(e, "attr", s[7]),
            z(e, "base", s[6]),
            z(e, "extra", s[1] && s[1].length),
            z(e, "mainProp", s[10] == s[2].simpleName),
            z(e, "subProp", s[9] == s[2].simpleName),
            z(e, "highlight", s[3])
        },
        m(N, G) {
            M(N, e, G),
            p && p.m(e, null),
            g(e, l),
            g(e, t),
            D && D.m(t, null),
            g(t, a),
            Q(i, t, null),
            g(e, r),
            w && w.m(e, null),
            g(e, o),
            g(e, n),
            _ && _.m(n, null),
            g(n, c),
            g(e, u),
            T && T.m(e, null),
            m = !0,
            A || (P = [mt(e, "click", s[13]), mt(e, "mouseleave", s[17]), mt(e, "mouseenter", s[18])],
            A = !0)
        },
        p(N, G) {
            var x;
            N[7] ? p || (p = _l(),
            p.c(),
            p.m(e, l)) : p && (p.d(1),
            p = null),
            N[1] ? D ? (D.p(N, G),
            G & 2 && I(D, 1)) : (D = ml(N),
            D.c(),
            I(D, 1),
            D.m(t, a)) : D && (me(),
            y(D, 1, 1, () => {
                D = null
            }
            ),
            de());
            const ae = {};
            G & 4 && (ae.prop = N[2]),
            i.$set(ae),
            N[5] ? w ? w.p(N, G) : (w = gl(N),
            w.c(),
            w.m(e, o)) : w && (w.d(1),
            w = null),
            N[0] ? _ || (_ = pl(),
            _.c(),
            _.m(n, c)) : _ && (_.d(1),
            _ = null),
            (!m || G & 4) && f !== (f = N[2].formatted + "") && Fe(c, f),
            T && T.p && (!m || G & 2097152) && Da(T, V, N, N[21], m ? $a(V, N[21], G, Ja) : Sa(N[21]), fl),
            (!m || G & 2) && te(e, "--extra", ((x = N[1]) == null ? void 0 : x.length) || 0),
            (!m || G & 256) && z(e, "primary", N[8]),
            (!m || G & 16) && z(e, "soft", N[4]),
            (!m || G & 32) && z(e, "full", N[5]),
            (!m || G & 128) && z(e, "attr", N[7]),
            (!m || G & 64) && z(e, "base", N[6]),
            (!m || G & 2) && z(e, "extra", N[1] && N[1].length),
            (!m || G & 1028) && z(e, "mainProp", N[10] == N[2].simpleName),
            (!m || G & 516) && z(e, "subProp", N[9] == N[2].simpleName),
            (!m || G & 8) && z(e, "highlight", N[3])
        },
        i(N) {
            m || (I(D),
            I(i.$$.fragment, N),
            I(T, N),
            m = !0)
        },
        o(N) {
            y(D),
            y(i.$$.fragment, N),
            y(T, N),
            m = !1
        },
        d(N) {
            N && h(e),
            p && p.d(),
            D && D.d(),
            Y(i),
            w && w.d(),
            _ && _.d(),
            T && T.d(N),
            A = !1,
            ua(P)
        }
    }
}
function _l(s) {
    let e;
    return {
        c() {
            e = b("div"),
            this.h()
        },
        l(l) {
            e = k(l, "DIV", {
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "bg svelte-g2rt2f")
        },
        m(l, t) {
            M(l, e, t)
        },
        d(l) {
            l && h(e)
        }
    }
}
function ml(s) {
    let e, l, t = ee(s[1]), a = [];
    for (let r = 0; r < t.length; r += 1)
        a[r] = dl(ul(s, t, r));
    const i = r => y(a[r], 1, 1, () => {
        a[r] = null
    }
    );
    return {
        c() {
            e = b("div");
            for (let r = 0; r < a.length; r += 1)
                a[r].c();
            this.h()
        },
        l(r) {
            e = k(r, "DIV", {
                class: !0
            });
            var o = E(e);
            for (let n = 0; n < a.length; n += 1)
                a[n].l(o);
            o.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "extras svelte-g2rt2f")
        },
        m(r, o) {
            M(r, e, o);
            for (let n = 0; n < a.length; n += 1)
                a[n] && a[n].m(e, null);
            l = !0
        },
        p(r, o) {
            if (o & 2) {
                t = ee(r[1]);
                let n;
                for (n = 0; n < t.length; n += 1) {
                    const f = ul(r, t, n);
                    a[n] ? (a[n].p(f, o),
                    I(a[n], 1)) : (a[n] = dl(f),
                    a[n].c(),
                    I(a[n], 1),
                    a[n].m(e, null))
                }
                for (me(),
                n = t.length; n < a.length; n += 1)
                    i(n);
                de()
            }
        },
        i(r) {
            if (!l) {
                for (let o = 0; o < t.length; o += 1)
                    I(a[o]);
                l = !0
            }
        },
        o(r) {
            a = a.filter(Boolean);
            for (let o = 0; o < a.length; o += 1)
                y(a[o]);
            l = !1
        },
        d(r) {
            r && h(e),
            Pe(a, r)
        }
    }
}
function dl(s) {
    let e, l;
    return e = new ma({
        props: {
            prop: s[2]
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a & 2 && (i.prop = t[2]),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function gl(s) {
    let e, l = s[11](s[2].simpleName) + "", t, a, i;
    return {
        c() {
            e = b("div"),
            t = De(l),
            a = H(),
            i = b("i"),
            this.h()
        },
        l(r) {
            e = k(r, "DIV", {
                class: !0
            });
            var o = E(e);
            t = Se(o, l),
            o.forEach(h),
            a = R(r),
            i = k(r, "I", {
                class: !0
            }),
            E(i).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "name svelte-g2rt2f"),
            d(i, "class", "svelte-g2rt2f")
        },
        m(r, o) {
            M(r, e, o),
            g(e, t),
            M(r, a, o),
            M(r, i, o)
        },
        p(r, o) {
            o & 2052 && l !== (l = r[11](r[2].simpleName) + "") && Fe(t, l)
        },
        d(r) {
            r && (h(e),
            h(a),
            h(i))
        }
    }
}
function pl(s) {
    let e;
    return {
        c() {
            e = De("+")
        },
        l(l) {
            e = Se(l, "+")
        },
        m(l, t) {
            M(l, e, t)
        },
        d(l) {
            l && h(e)
        }
    }
}
function Xa(s) {
    let e, l, t = s[2] && hl(s);
    return {
        c() {
            t && t.c(),
            e = Oe()
        },
        l(a) {
            t && t.l(a),
            e = Oe()
        },
        m(a, i) {
            t && t.m(a, i),
            M(a, e, i),
            l = !0
        },
        p(a, [i]) {
            a[2] ? t ? (t.p(a, i),
            i & 4 && I(t, 1)) : (t = hl(a),
            t.c(),
            I(t, 1),
            t.m(e.parentNode, e)) : t && (me(),
            y(t, 1, 1, () => {
                t = null
            }
            ),
            de())
        },
        i(a) {
            l || (I(t),
            l = !0)
        },
        o(a) {
            y(t),
            l = !1
        },
        d(a) {
            a && h(e),
            t && t.d(a)
        }
    }
}
function Za(s, e, l) {
    let t, a, i, r, o, n, f, c, u, m, A, {$$slots: P={}, $$scope: p} = e;
    const {ef: D} = at("l10n");
    ve(s, D, L => l(11, A = L));
    let {prop: w=null} = e
      , {type: _="base"} = e
      , {plus: V=!1} = e
      , {extra: T=null} = e;
    function N() {
        console.log(w)
    }
    const G = at("mainProp");
    ve(s, G, L => l(10, m = L));
    const ae = at("subProp");
    ve(s, ae, L => l(9, u = L));
    const x = at("highlight");
    ve(s, x, L => l(20, c = L));
    function $() {
        lt(x, c = [], c)
    }
    function O() {
        if (w.id == J.ArtsDamageIncrease) {
            lt(x, c = [...q.arts, "ArtsDamageIncrease"], c);
            return
        }
        if (w.id == J.AllSkillDamageIncrease) {
            lt(x, c = [...q.skills, "AllSkillDamageIncrease"], c);
            return
        }
        w.isArts ? lt(x, c = [w.simpleName, "ArtsDamageIncrease"], c) : w.isSkill ? lt(x, c = [w.simpleName, "AllSkillDamageIncrease"], c) : lt(x, c = [w.simpleName], c),
        T && T.length && c.push(...T.map(L => L.simpleName)),
        i && c.includes("Atk") ? c.push(m, u) : i && c.includes("MaxHp") ? c.push("Str") : i && c.includes("HealTakenIncrease") && c.push("Will")
    }
    function B(L, ge) {
        return a && ge.includes("Atk") && L.simpleName != "Atk" || a && ge.includes("MaxHp") && L.simpleName != "MaxHp" || a && ge.includes("HealTakenIncrease") && L.simpleName != "HealTakenIncrease" ? !1 : ge.includes(L.simpleName) || ge.some(fe => n == null ? void 0 : n.includes(fe))
    }
    return s.$$set = L => {
        "prop"in L && l(2, w = L.prop),
        "type"in L && l(19, _ = L.type),
        "plus"in L && l(0, V = L.plus),
        "extra"in L && l(1, T = L.extra),
        "$$scope"in L && l(21, p = L.$$scope)
    }
    ,
    s.$$.update = () => {
        s.$$.dirty & 524288 && l(8, t = _ == "primary"),
        s.$$.dirty & 524288 && l(4, a = _ == "soft"),
        s.$$.dirty & 524288 && l(5, i = _ == "full"),
        s.$$.dirty & 524288 && l(7, r = _ == "attr"),
        s.$$.dirty & 524288 && l(6, o = _ == "base"),
        s.$$.dirty & 4 && xt[w.simpleName],
        s.$$.dirty & 2 && (n = T == null ? void 0 : T.map(L => L.simpleName)),
        s.$$.dirty & 1048580 && l(3, f = B(w, c))
    }
    ,
    [V, T, w, f, a, i, o, r, t, u, m, A, D, N, G, ae, x, $, O, _, c, p, P]
}
class St extends Ye {
    constructor(e) {
        super(),
        Je(this, e, Za, Xa, Qe, {
            prop: 2,
            type: 19,
            plus: 0,
            extra: 1
        })
    }
}
class tt {
    constructor() {}
    static avatar(e) {
        const l = new je("avatar");
        for (const t in e.meta.excel.BaseAttributes) {
            const a = e.meta.excel.BaseAttributes[t]
              , i = a.BaseValue
              , r = a.AddValue * (e.level - 1)
              , o = i + r;
            l.add(J[t], o)
        }
        return l.add("MaxHp_base", e.meta.excel.BaseHpByLevel[e.level - 1]),
        l.add("Atk_base", e.meta.excel.BaseAtkByLevel[e.level - 1]),
        l.add("UltimateSpGainScalar_base", 1),
        l.add("CriticalDamageIncrease_base", .5),
        l
    }
    static weapon(e) {
        const l = new je("weapon");
        if (!e)
            return l;
        const a = e.stats().baseAtk.value;
        return l.add("Atk_base", a),
        l
    }
    static weaponAffixes(e, l) {
        const t = new je("weaponAffixes");
        if (!l)
            return t;
        const a = l.stats();
        for (var i of a.skillStats)
            for (var r of i) {
                if (!r.prop || !r.formula)
                    continue;
                const o = new q(r.prop.convert(e),0).remake(r.formula).id
                  , n = r.prop.value;
                t.add(J[o], n)
            }
        return t
    }
    static equips(e, l) {
        const t = new je("equips");
        for (const i of e) {
            if (!i)
                continue;
            const r = i.stats();
            for (var a of r) {
                const o = a.convert(l);
                t.add(J[o], a.value)
            }
        }
        return t
    }
    static equipSuit(e) {
        const l = new je("equipSuit")
          , t = {};
        for (const a of e) {
            if (!a)
                continue;
            const i = a.meta.excel.SuitId;
            i && (t[i] || (t[i] = {
                set: a.meta.set,
                count: 0
            }),
            t[i].count++)
        }
        for (const a in t) {
            const i = t[a];
            if (i.count >= 3) {
                const r = i.set.SkillId
                  , o = Va[r];
                for (const n in o.PropMap) {
                    const f = o.PropMap[n]
                      , c = f.Values[0]
                      , u = f.Formula
                      , m = new q(n,c).remake(u);
                    l.add(J[m.id], m.value)
                }
            }
        }
        return l
    }
    static attributeConversion(e) {
        const l = new je("attributeConversion")
          , t = e.sum()
          , a = t.Str * 5;
        l.add("MaxHp_base", a);
        const i = Math.min(90, 100 - 100 / (t.Agi * .001 + 1));
        l.add("PhysicalDmgResistScalar_delta", i);
        const r = Math.min(90, 100 - 100 / (t.Wisd * .001 + 1));
        l.add("CrystDmgResistScalar_delta", r),
        l.add("PulseDmgResistScalar_delta", r),
        l.add("NaturalDmgResistScalar_delta", r),
        l.add("FireDmgResistScalar_delta", r);
        const o = t.Will * .001;
        return l.add("HealTakenIncrease_delta", o),
        l
    }
    static attributeAtkConversion(e, l) {
        const t = new je("attributeAtkConversion")
          , a = l.sum()
          , i = {
            39: a.Str,
            40: a.Agi,
            41: a.Wisd,
            42: a.Will
        };
        e.meta.excel.MainAttrId in i || console.warn("Main attr lookup failed:", e.meta.excel.MainAttrId);
        const r = i[e.meta.excel.MainAttrId];
        e.meta.excel.SubAttrId in i || console.warn("Sub attr lookup failed:", e.meta.excel.SubAttrId);
        const o = i[e.meta.excel.SubAttrId]
          , n = r * .005 + o * .002;
        return t.add("Atk_total_ratio", n),
        t
    }
    static pots(e) {
        const l = new je("pots");
        for (const t of e.meta.excel.PotAttributes)
            if (!(e.const < t.Level))
                for (const a in t.Attrs) {
                    const i = t.Attrs[a]
                      , r = new q(a,i.Value).remake(i.Formula);
                    l.add(J[r.id], r.value)
                }
        return l
    }
    static skills(e) {
        const l = new je("skills")
          , t = {}
          , a = e.meta.excel.AttributeNodes
          , i = Object.values(a)[0]
          , r = Object.keys(i)[0];
        t[r] = 0,
        e.data.talent.attrNodes.forEach(f => {
            for (var c in e.meta.excel.AttributeNodes[f])
                t[c] || (t[c] = 0),
                t[c] += e.meta.excel.AttributeNodes[f][c]
        }
        );
        const o = Object.keys(t)[0]
          , n = t[o];
        return l.add(J[o], n),
        l
    }
    static corrections(e, l) {
        const t = new je("corrections")
          , a = l.sum();
        switch (e.meta.id) {
        case "35":
            if (e.data.talent.latestPassiveSkillNodes.includes("chr_0020_meurs_passive_skill_0_1")) {
                var i = Math.floor(a.Will / 10) * 1;
                t.add("Def_delta", i)
            } else if (e.data.talent.latestPassiveSkillNodes.includes("chr_0020_meurs_passive_skill_0_2")) {
                var i = Math.floor(a.Will / 10) * 1.2;
                t.add("Def_delta", i)
            }
            break;
        case "12":
            e.data.talent.latestPassiveSkillNodes.includes("chr_0013_aglina_passive_skill_0_1") ? t.add("UltimateSpGainScalar_delta", .04) : e.data.talent.latestPassiveSkillNodes.includes("chr_0013_aglina_passive_skill_0_2") && t.add("UltimateSpGainScalar_delta", .07),
            (e.data.talent.latestPassiveSkillNodes.includes("chr_0013_aglina_passive_skill_0_1") || e.data.talent.latestPassiveSkillNodes.includes("chr_0013_aglina_passive_skill_0_2") || e.data.potentialLevel >= 3) && t.add("UltimateSpGainScalar_delta", .05);
            break;
        case "26":
            if (e.data.talent.latestPassiveSkillNodes.includes("chr_0015_lifeng_passive_skill_0_1")) {
                var i = (a.Wisd + a.Will) * .001;
                t.add("Atk_total_ratio", i)
            } else if (e.data.talent.latestPassiveSkillNodes.includes("chr_0015_lifeng_passive_skill_0_2")) {
                var i = (a.Wisd + a.Will) * .0015;
                t.add("Atk_total_ratio", i)
            }
            break
        }
        return t
    }
}
class je {
    constructor(e=Math.random().toString(36).substring(7)) {
        this.id = "",
        this.disabled = !1,
        this.Main = 0,
        this.Sub = 0,
        this.Level = 0,
        this.MaxHp_base = 0,
        this.MaxHp_ratio = 0,
        this.MaxHp_delta = 0,
        this.Atk_base = 0,
        this.Atk_ratio = 0,
        this.Atk_delta = 0,
        this.Atk_total_ratio = 0,
        this.Def_base = 0,
        this.Def_ratio = 0,
        this.Def_delta = 0,
        this.PhysicalDamageTakenScalar_base = 0,
        this.PhysicalDamageTakenScalar_delta = 0,
        this.FireDamageTakenScalar_base = 0,
        this.FireDamageTakenScalar_delta = 0,
        this.PulseDamageTakenScalar_base = 0,
        this.PulseDamageTakenScalar_delta = 0,
        this.CrystDamageTakenScalar_base = 0,
        this.CrystDamageTakenScalar_delta = 0,
        this.Weight = 0,
        this.CriticalRate_base = 0,
        this.CriticalRate_delta = 0,
        this.CriticalDamageIncrease_base = 0,
        this.CriticalDamageIncrease_delta = 0,
        this.Hatred = 0,
        this.NormalAttackRange = 0,
        this.MoveSpeedScalar = 0,
        this.TurnRateScalar = 0,
        this.AttackRate = 0,
        this.SkillCooldownScalar = 0,
        this.NormalAttackDamageIncrease_base = 0,
        this.NormalAttackDamageIncrease_delta = 0,
        this.HpRecoveryPerSec = 0,
        this.HpRecoveryPerSecByMaxHpRatio = 0,
        this.MaxPoise = 0,
        this.PoiseRecTime = 0,
        this.MaxUltimateSp = 0,
        this.DamageTakenScalarWithPoise = 0,
        this.PoiseDamageTakenScalar = 0,
        this.PhysicalInflictionDamageScalar = 0,
        this.PoiseDamageOutputScalar_base = 0,
        this.PoiseDamageOutputScalar_delta = 0,
        this.BreakingAttackDamageTakenScalar = 0,
        this.UltimateSkillDamageIncrease_base = 0,
        this.UltimateSkillDamageIncrease_delta = 0,
        this.HealOutputIncrease_base = 0,
        this.HealOutputIncrease_delta = 0,
        this.HealTakenIncrease_base = 0,
        this.HealTakenIncrease_delta = 0,
        this.PoiseRecTimeScalar = 0,
        this.NormalSkillDamageIncrease_base = 0,
        this.NormalSkillDamageIncrease_delta = 0,
        this.ComboSkillDamageIncrease_base = 0,
        this.ComboSkillDamageIncrease_delta = 0,
        this.KnockDownTimeAddition = 0,
        this.FireBurstDamageIncrease_base = 0,
        this.FireBurstDamageIncrease_delta = 0,
        this.PulseBurstDamageIncrease_base = 0,
        this.PulseBurstDamageIncrease_delta = 0,
        this.CrystBurstDamageIncrease_base = 0,
        this.CrystBurstDamageIncrease_delta = 0,
        this.NaturalBurstDamageIncrease_base = 0,
        this.NaturalBurstDamageIncrease_delta = 0,
        this.Str_base = 0,
        this.Str_ratio = 0,
        this.Str_delta = 0,
        this.Agi_base = 0,
        this.Agi_ratio = 0,
        this.Agi_delta = 0,
        this.Wisd_base = 0,
        this.Wisd_ratio = 0,
        this.Wisd_delta = 0,
        this.Will_base = 0,
        this.Will_ratio = 0,
        this.Will_delta = 0,
        this.LifeSteal = 0,
        this.UltimateSpGainScalar_base = 0,
        this.UltimateSpGainScalar_delta = 0,
        this.AtbCostAddition = 0,
        this.SkillCooldownAddition = 0,
        this.ComboSkillCooldownScalar_base = 0,
        this.ComboSkillCooldownScalar_delta = 0,
        this.NaturalDamageTakenScalar_base = 0,
        this.NaturalDamageTakenScalar_delta = 0,
        this.IgniteDamageScalar = 0,
        this.PhysicalDamageIncrease_base = 0,
        this.PhysicalDamageIncrease_delta = 0,
        this.FireDamageIncrease_base = 0,
        this.FireDamageIncrease_delta = 0,
        this.PulseDamageIncrease_base = 0,
        this.PulseDamageIncrease_delta = 0,
        this.CrystDamageIncrease_base = 0,
        this.CrystDamageIncrease_delta = 0,
        this.NaturalDamageIncrease_base = 0,
        this.NaturalDamageIncrease_delta = 0,
        this.EtherDamageIncrease_base = 0,
        this.EtherDamageIncrease_delta = 0,
        this.FireAbnormalDamageIncrease_base = 0,
        this.FireAbnormalDamageIncrease_delta = 0,
        this.PulseAbnormalDamageIncrease_base = 0,
        this.PulseAbnormalDamageIncrease_delta = 0,
        this.CrystAbnormalDamageIncrease_base = 0,
        this.CrystAbnormalDamageIncrease_delta = 0,
        this.NaturalAbnormalDamageIncrease_base = 0,
        this.NaturalAbnormalDamageIncrease_delta = 0,
        this.EtherDamageTakenScalar_base = 0,
        this.EtherDamageTakenScalar_delta = 0,
        this.DamageToBrokenUnitIncrease_base = 0,
        this.DamageToBrokenUnitIncrease_delta = 0,
        this.WeaknessDmgScalar = 0,
        this.ShelterDmgScalar = 0,
        this.PhysicalEnhancedDmgIncrease = 0,
        this.FireEnhancedDmgIncrease = 0,
        this.PulseEnhancedDmgIncrease = 0,
        this.CrystEnhancedDmgIncrease = 0,
        this.NaturalEnhancedDmgIncrease = 0,
        this.EtherEnhancedDmgIncrease = 0,
        this.PhysicalVulnerableDmgIncrease = 0,
        this.FireVulnerableDmgIncrease = 0,
        this.PulseVulnerableDmgIncrease = 0,
        this.CrystVulnerableDmgIncrease = 0,
        this.NaturalVulnerableDmgIncrease = 0,
        this.EtherVulnerableDmgIncrease = 0,
        this.AtkIncreaseFactorFromStr = 0,
        this.AtkIncreaseFactorFromAgi = 0,
        this.AtkIncreaseFactorFromWisd = 0,
        this.AtkIncreaseFactorFromWill = 0,
        this.PhysicalDmgResistScalar_base = 0,
        this.PhysicalDmgResistScalar_delta = 0,
        this.NaturalDmgResistScalar_base = 0,
        this.NaturalDmgResistScalar_delta = 0,
        this.CrystDmgResistScalar_base = 0,
        this.CrystDmgResistScalar_delta = 0,
        this.PulseDmgResistScalar_base = 0,
        this.PulseDmgResistScalar_delta = 0,
        this.FireDmgResistScalar_base = 0,
        this.FireDmgResistScalar_delta = 0,
        this.EtherDmgResistScalar_base = 0,
        this.EtherDmgResistScalar_delta = 0,
        this.SlowActionSpeedScalar = 0,
        this.PhysicalAndSpellInflictionEnhance_base = 0,
        this.PhysicalAndSpellInflictionEnhance_delta = 0,
        this.ShieldOutputIncrease = 0,
        this.ShieldTakenIncrease = 0,
        this.NormalAttackStartRange = 0,
        this.id = e
    }
    add(e, l) {
        if (e !== "id" && e !== "disabled") {
            if (this[e] === void 0)
                return console.trace("Invalid prop name:", e, "value:", l);
            isNaN(this[e] + l) && console.trace("Addition resulted in NaN:", this[e], "+", l),
            this[e] = this[e] + l
        }
    }
    get props() {
        return [new q(J.Str_base,this.Str), new q(J.Agi_base,this.Agi), new q(J.Wisd_base,this.Wisd), new q(J.Will_base,this.Will), new q(J.MaxHp_base,this.MaxHp), new q(J.Atk_base,this.Atk), new q(J.Def_base,this.Def), new q(J.CriticalRate_base,this.CriticalRate), new q(J.CriticalDamageIncrease_base,this.CriticalDamage), new q(J.PhysicalAndSpellInflictionEnhance_base,this.PhysicalAndSpellInflictionEnhance), new q(J.HealOutputIncrease_base,this.HealOutputIncrease), new q(J.HealTakenIncrease_base,this.HealTakenIncrease), new q(J.ComboSkillCooldownScalar_base,this.ComboSkillCooldownScalar), new q(J.UltimateSpGainScalar_base,this.UltimateSpGainScalar), new q(J.PoiseDamageOutputScalar_base,this.PoiseDamageOutputScalar), new q(J.DamageToBrokenUnitIncrease_base,this.DamageToBrokenUnitIncrease), new q(J.PhysicalDamageIncrease_base,this.PhysicalDamageIncrease), new q(J.FireDamageIncrease_base,this.FireDamageIncrease), new q(J.PulseDamageIncrease_base,this.PulseDamageIncrease), new q(J.CrystDamageIncrease_base,this.CrystDamageIncrease), new q(J.NaturalDamageIncrease_base,this.NaturalDamageIncrease), new q(J.NormalAttackDamageIncrease_base,this.NormalAttackDamageIncrease), new q(J.NormalSkillDamageIncrease_base,this.NormalSkillDamageIncrease), new q(J.ComboSkillDamageIncrease_base,this.ComboSkillDamageIncrease), new q(J.UltimateSkillDamageIncrease_base,this.UltimateSkillDamageIncrease)]
    }
    get MaxHp() {
        return Math.floor(this.MaxHp_base * (1 + this.MaxHp_ratio) + this.MaxHp_delta)
    }
    get Atk() {
        return Math.floor(this.AtkBasicTotal * (1 + this.Atk_total_ratio))
    }
    get AtkBasicTotal() {
        return this.Atk_base * (1 + this.Atk_ratio) + this.Atk_delta
    }
    get Def() {
        return Math.floor(this.Def_base * (1 + this.Def_ratio) + this.Def_delta)
    }
    get CriticalRate() {
        return this.CriticalRate_base + this.CriticalRate_delta
    }
    get CriticalDamage() {
        return this.CriticalDamageIncrease_base + this.CriticalDamageIncrease_delta
    }
    get PhysicalDamageIncrease() {
        return this.PhysicalDamageIncrease_base + this.PhysicalDamageIncrease_delta
    }
    get FireDamageIncrease() {
        return this.FireDamageIncrease_base + this.FireDamageIncrease_delta
    }
    get CrystDamageIncrease() {
        return this.CrystDamageIncrease_base + this.CrystDamageIncrease_delta
    }
    get NaturalDamageIncrease() {
        return this.NaturalDamageIncrease_base + this.NaturalDamageIncrease_delta
    }
    get PulseDamageIncrease() {
        return this.PulseDamageIncrease_base + this.PulseDamageIncrease_delta
    }
    get PhysicalAndSpellInflictionEnhance() {
        return this.PhysicalAndSpellInflictionEnhance_base + this.PhysicalAndSpellInflictionEnhance_delta
    }
    get HealOutputIncrease() {
        return this.HealOutputIncrease_base + this.HealOutputIncrease_delta
    }
    get HealTakenIncrease() {
        return this.HealTakenIncrease_base + this.HealTakenIncrease_delta
    }
    get ComboSkillCooldownScalar() {
        return this.ComboSkillCooldownScalar_base + this.ComboSkillCooldownScalar_delta
    }
    get UltimateSpGainScalar() {
        return this.UltimateSpGainScalar_base + this.UltimateSpGainScalar_delta
    }
    get DamageToBrokenUnitIncrease() {
        return this.DamageToBrokenUnitIncrease_base + this.DamageToBrokenUnitIncrease_delta
    }
    get PoiseDamageOutputScalar() {
        return this.PoiseDamageOutputScalar_base + this.PoiseDamageOutputScalar_delta
    }
    get NormalAttackDamageIncrease() {
        return this.NormalAttackDamageIncrease_base + this.NormalAttackDamageIncrease_delta
    }
    get NormalSkillDamageIncrease() {
        return this.NormalSkillDamageIncrease_base + this.NormalSkillDamageIncrease_delta
    }
    get ComboSkillDamageIncrease() {
        return this.ComboSkillDamageIncrease_base + this.ComboSkillDamageIncrease_delta
    }
    get UltimateSkillDamageIncrease() {
        return this.UltimateSkillDamageIncrease_base + this.UltimateSkillDamageIncrease_delta
    }
    get Str() {
        return Math.floor(this.Str_base * (1 + this.Str_ratio) + this.Str_delta)
    }
    get Agi() {
        return Math.floor(this.Agi_base * (1 + this.Agi_ratio) + this.Agi_delta)
    }
    get Wisd() {
        return Math.floor(this.Wisd_base * (1 + this.Wisd_ratio) + this.Wisd_delta)
    }
    get Will() {
        return Math.floor(this.Will_base * (1 + this.Will_ratio) + this.Will_delta)
    }
}
class xa {
    constructor() {
        this.layers = new Map
    }
    sum(...e) {
        let l = new je;
        return this.layers.forEach(t => {
            if (!t.disabled && !(e.length && !e.includes(t.id)))
                for (let a in t) {
                    if (a === "id" || a === "disabled")
                        continue;
                    let i = t[a];
                    l[a] += i
                }
        }
        ),
        l
    }
    add(e) {
        this.layers.set(e.id, e)
    }
    clear() {
        this.layers.clear()
    }
    disable(e) {
        this.layers.get(e).disabled = !0
    }
    enable(e) {
        this.layers.get(e).disabled = !1
    }
    toggle(e) {
        const l = this.layers.get(e);
        return l.disabled = !l.disabled,
        l.disabled
    }
}
function es(s) {
    let e, l, t;
    return l = new Mt({
        props: {
            name: "SkillMastery"
        }
    }),
    {
        c() {
            e = b("div"),
            j(l.$$.fragment),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0,
                "data-level": !0
            });
            var i = E(e);
            K(l.$$.fragment, i),
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "SkillMastery svelte-99v3l2"),
            d(e, "data-level", s[0]),
            z(e, "shade", s[1])
        },
        m(a, i) {
            M(a, e, i),
            Q(l, e, null),
            t = !0
        },
        p(a, [i]) {
            (!t || i & 1) && d(e, "data-level", a[0]),
            (!t || i & 2) && z(e, "shade", a[1])
        },
        i(a) {
            t || (I(l.$$.fragment, a),
            t = !0)
        },
        o(a) {
            y(l.$$.fragment, a),
            t = !1
        },
        d(a) {
            a && h(e),
            Y(l)
        }
    }
}
function ts(s, e, l) {
    let {level: t=0} = e
      , {shade: a=!0} = e;
    return s.$$set = i => {
        "level"in i && l(0, t = i.level),
        "shade"in i && l(1, a = i.shade)
    }
    ,
    [t, a]
}
class ls extends Ye {
    constructor(e) {
        super(),
        Je(this, e, ts, es, Qe, {
            level: 0,
            shade: 1
        })
    }
}
function vl(s, e, l) {
    var o, n;
    const t = s.slice();
    t[22] = e[l].id,
    t[16] = e[l].level,
    t[18] = l;
    const a = t[2][t[18]];
    t[23] = a;
    const i = (o = t[0].meta.excel.SkillInfoMap[t[22]]) == null ? void 0 : o.Icon;
    t[24] = i;
    const r = (n = t[0].meta.excel.SkillInfoMap[t[22]]) == null ? void 0 : n.Element;
    return t[25] = r,
    t
}
function as(s) {
    const e = s.slice()
      , l = e[16] - 9;
    return e[27] = l,
    e
}
function bl(s, e, l) {
    const t = s.slice();
    t[14] = e[l][0],
    t[15] = e[l][1],
    t[18] = l;
    const a = t[5][t[15].Index];
    return t[16] = a,
    t
}
function kl(s, e, l) {
    const t = s.slice();
    return t[19] = e[l],
    t
}
function ss(s) {
    let e, l, t = ee(s[0].skills), a = [];
    for (let r = 0; r < t.length; r += 1)
        a[r] = Sl(vl(s, t, r));
    const i = r => y(a[r], 1, 1, () => {
        a[r] = null
    }
    );
    return {
        c() {
            e = b("div");
            for (let r = 0; r < a.length; r += 1)
                a[r].c();
            this.h()
        },
        l(r) {
            e = k(r, "DIV", {
                class: !0
            });
            var o = E(e);
            for (let n = 0; n < a.length; n += 1)
                a[n].l(o);
            o.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "battle svelte-mpem34")
        },
        m(r, o) {
            M(r, e, o);
            for (let n = 0; n < a.length; n += 1)
                a[n] && a[n].m(e, null);
            l = !0
        },
        p(r, o) {
            if (o & 5) {
                t = ee(r[0].skills);
                let n;
                for (n = 0; n < t.length; n += 1) {
                    const f = vl(r, t, n);
                    a[n] ? (a[n].p(f, o),
                    I(a[n], 1)) : (a[n] = Sl(f),
                    a[n].c(),
                    I(a[n], 1),
                    a[n].m(e, null))
                }
                for (me(),
                n = t.length; n < a.length; n += 1)
                    i(n);
                de()
            }
        },
        i(r) {
            if (!l) {
                for (let o = 0; o < t.length; o += 1)
                    I(a[o]);
                l = !0
            }
        },
        o(r) {
            a = a.filter(Boolean);
            for (let o = 0; o < a.length; o += 1)
                y(a[o]);
            l = !1
        },
        d(r) {
            r && h(e),
            Pe(a, r)
        }
    }
}
function is(s) {
    let e, l, t = s[3] && $l(s), a = ee(s[6]), i = [];
    for (let r = 0; r < a.length; r += 1)
        i[r] = wl(bl(s, a, r));
    return {
        c() {
            e = b("div"),
            t && t.c(),
            l = H();
            for (let r = 0; r < i.length; r += 1)
                i[r].c();
            this.h()
        },
        l(r) {
            e = k(r, "DIV", {
                class: !0
            });
            var o = E(e);
            t && t.l(o),
            l = R(o);
            for (let n = 0; n < i.length; n += 1)
                i[n].l(o);
            o.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "nodes svelte-mpem34")
        },
        m(r, o) {
            M(r, e, o),
            t && t.m(e, null),
            g(e, l);
            for (let n = 0; n < i.length; n += 1)
                i[n] && i[n].m(e, null)
        },
        p(r, o) {
            if (r[3] ? t ? t.p(r, o) : (t = $l(r),
            t.c(),
            t.m(e, l)) : t && (t.d(1),
            t = null),
            o & 96) {
                a = ee(r[6]);
                let n;
                for (n = 0; n < a.length; n += 1) {
                    const f = bl(r, a, n);
                    i[n] ? i[n].p(f, o) : (i[n] = wl(f),
                    i[n].c(),
                    i[n].m(e, null))
                }
                for (; n < i.length; n += 1)
                    i[n].d(1);
                i.length = a.length
            }
        },
        i: be,
        o: be,
        d(r) {
            r && h(e),
            t && t.d(),
            Pe(i, r)
        }
    }
}
function Il(s) {
    let e, l, t, a, i, r, o, n, f, c, u, m, A;
    const P = [ns, rs]
      , p = [];
    function D(V, T) {
        return V[16] > 9 ? 0 : 1
    }
    function w(V, T) {
        return T === 0 ? as(V) : V
    }
    f = D(s),
    c = p[f] = P[f](w(s, f));
    let _ = s[23].value > 0 && Dl(s);
    return {
        c() {
            e = b("div"),
            l = b("div"),
            t = H(),
            a = b("div"),
            i = H(),
            r = b("div"),
            o = H(),
            n = b("div"),
            c.c(),
            u = H(),
            _ && _.c(),
            m = H(),
            this.h()
        },
        l(V) {
            e = k(V, "DIV", {
                class: !0,
                style: !0
            });
            var T = E(e);
            l = k(T, "DIV", {
                class: !0
            }),
            E(l).forEach(h),
            t = R(T),
            a = k(T, "DIV", {
                class: !0,
                style: !0
            }),
            E(a).forEach(h),
            i = R(T),
            r = k(T, "DIV", {
                class: !0
            }),
            E(r).forEach(h),
            o = R(T),
            n = k(T, "DIV", {
                class: !0
            });
            var N = E(n);
            c.l(N),
            N.forEach(h),
            u = R(T),
            _ && _.l(T),
            m = R(T),
            T.forEach(h),
            this.h()
        },
        h() {
            d(l, "class", "deco svelte-mpem34"),
            d(a, "class", "bg svelte-mpem34"),
            te(a, "--elementColor", xt[s[25]]),
            z(a, "full", s[18] == 3),
            d(r, "class", "icon svelte-mpem34"),
            d(n, "class", "level svelte-mpem34"),
            d(e, "class", "Skill svelte-mpem34"),
            te(e, "--icon", "url(" + s[24] + ")")
        },
        m(V, T) {
            M(V, e, T),
            g(e, l),
            g(e, t),
            g(e, a),
            g(e, i),
            g(e, r),
            g(e, o),
            g(e, n),
            p[f].m(n, null),
            g(e, u),
            _ && _.m(e, null),
            g(e, m),
            A = !0
        },
        p(V, T) {
            (!A || T & 1) && te(a, "--elementColor", xt[V[25]]);
            let N = f;
            f = D(V),
            f === N ? p[f].p(w(V, f), T) : (me(),
            y(p[N], 1, 1, () => {
                p[N] = null
            }
            ),
            de(),
            c = p[f],
            c ? c.p(w(V, f), T) : (c = p[f] = P[f](w(V, f)),
            c.c()),
            I(c, 1),
            c.m(n, null)),
            V[23].value > 0 ? _ ? (_.p(V, T),
            T & 4 && I(_, 1)) : (_ = Dl(V),
            _.c(),
            I(_, 1),
            _.m(e, m)) : _ && (me(),
            y(_, 1, 1, () => {
                _ = null
            }
            ),
            de()),
            (!A || T & 1) && te(e, "--icon", "url(" + V[24] + ")")
        },
        i(V) {
            A || (I(c),
            I(_),
            A = !0)
        },
        o(V) {
            y(c),
            y(_),
            A = !1
        },
        d(V) {
            V && h(e),
            p[f].d(),
            _ && _.d()
        }
    }
}
function rs(s) {
    let e = s[16] + "", l;
    return {
        c() {
            l = De(e)
        },
        l(t) {
            l = Se(t, e)
        },
        m(t, a) {
            M(t, l, a)
        },
        p(t, a) {
            a & 1 && e !== (e = t[16] + "") && Fe(l, e)
        },
        i: be,
        o: be,
        d(t) {
            t && h(l)
        }
    }
}
function ns(s) {
    let e, l;
    return e = new ls({
        props: {
            level: s[27]
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a & 1 && (i.level = t[27]),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function Dl(s) {
    let e, l, t;
    return l = new St({
        props: {
            prop: s[23],
            plus: !0,
            type: "soft"
        }
    }),
    {
        c() {
            e = b("div"),
            j(l.$$.fragment),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0
            });
            var i = E(e);
            K(l.$$.fragment, i),
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "prop svelte-mpem34")
        },
        m(a, i) {
            M(a, e, i),
            Q(l, e, null),
            t = !0
        },
        p(a, i) {
            const r = {};
            i & 4 && (r.prop = a[23]),
            l.$set(r)
        },
        i(a) {
            t || (I(l.$$.fragment, a),
            t = !0)
        },
        o(a) {
            y(l.$$.fragment, a),
            t = !1
        },
        d(a) {
            a && h(e),
            Y(l)
        }
    }
}
function Sl(s) {
    let e, l, t = s[24] && Il(s);
    return {
        c() {
            t && t.c(),
            e = Oe()
        },
        l(a) {
            t && t.l(a),
            e = Oe()
        },
        m(a, i) {
            t && t.m(a, i),
            M(a, e, i),
            l = !0
        },
        p(a, i) {
            a[24] ? t ? (t.p(a, i),
            i & 1 && I(t, 1)) : (t = Il(a),
            t.c(),
            I(t, 1),
            t.m(e.parentNode, e)) : t && (me(),
            y(t, 1, 1, () => {
                t = null
            }
            ),
            de())
        },
        i(a) {
            l || (I(t),
            l = !0)
        },
        o(a) {
            y(t),
            l = !1
        },
        d(a) {
            a && h(e),
            t && t.d(a)
        }
    }
}
function $l(s) {
    let e, l, t, a, i, r, o = s[3].value && Al(s);
    return {
        c() {
            e = b("div"),
            l = b("div"),
            a = H(),
            o && o.c(),
            this.h()
        },
        l(n) {
            e = k(n, "DIV", {
                class: !0
            });
            var f = E(e);
            l = k(f, "DIV", {
                class: !0,
                style: !0,
                "data-level": !0
            }),
            E(l).forEach(h),
            a = R(f),
            o && o.l(f),
            f.forEach(h),
            this.h()
        },
        h() {
            d(l, "class", "NodeSkill svelte-mpem34"),
            te(l, "--icon", "url(" + s[3].icon + ")"),
            d(l, "data-level", t = s[3].value),
            d(e, "class", "AttributeSkill svelte-mpem34"),
            z(e, "highlight", s[4])
        },
        m(n, f) {
            M(n, e, f),
            g(e, l),
            g(e, a),
            o && o.m(e, null),
            i || (r = [mt(e, "mouseleave", s[10]), mt(e, "mouseenter", s[11])],
            i = !0)
        },
        p(n, f) {
            f & 8 && te(l, "--icon", "url(" + n[3].icon + ")"),
            f & 8 && t !== (t = n[3].value) && d(l, "data-level", t),
            n[3].value ? o ? o.p(n, f) : (o = Al(n),
            o.c(),
            o.m(e, null)) : o && (o.d(1),
            o = null),
            f & 16 && z(e, "highlight", n[4])
        },
        d(n) {
            n && h(e),
            o && o.d(),
            i = !1,
            ua(r)
        }
    }
}
function Al(s) {
    let e, l, t = s[3].formatted + "", a;
    return {
        c() {
            e = b("span"),
            l = De("+"),
            a = De(t),
            this.h()
        },
        l(i) {
            e = k(i, "SPAN", {
                class: !0
            });
            var r = E(e);
            l = Se(r, "+"),
            a = Se(r, t),
            r.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "svelte-mpem34")
        },
        m(i, r) {
            M(i, e, r),
            g(e, l),
            g(e, a)
        },
        p(i, r) {
            r & 8 && t !== (t = i[3].formatted + "") && Fe(a, t)
        },
        d(i) {
            i && h(e)
        }
    }
}
function os(s) {
    let e, l, t, a, i = ee({
        length: s[16]
    }), r = [];
    for (let o = 0; o < i.length; o += 1)
        r[o] = El(kl(s, i, o));
    return {
        c() {
            e = b("div"),
            l = b("div");
            for (let o = 0; o < r.length; o += 1)
                r[o].c();
            t = H(),
            this.h()
        },
        l(o) {
            e = k(o, "DIV", {
                class: !0,
                style: !0,
                "data-level": !0
            });
            var n = E(e);
            l = k(n, "DIV", {
                class: !0
            });
            var f = E(l);
            for (let c = 0; c < r.length; c += 1)
                r[c].l(f);
            f.forEach(h),
            t = R(n),
            n.forEach(h),
            this.h()
        },
        h() {
            var o, n;
            d(l, "class", "upg svelte-mpem34"),
            d(e, "class", "NodeSkill svelte-mpem34"),
            te(e, "--icon", "url(" + ((n = (o = s[15]) == null ? void 0 : o.Icon) == null ? void 0 : n.replace("ef/", "ef/skillicon/")) + ")"),
            d(e, "data-level", a = s[16])
        },
        m(o, n) {
            M(o, e, n),
            g(e, l);
            for (let f = 0; f < r.length; f += 1)
                r[f] && r[f].m(l, null);
            g(e, t)
        },
        p(o, n) {
            var f, c;
            if (n & 96) {
                i = ee({
                    length: o[16]
                });
                let u;
                for (u = 0; u < i.length; u += 1) {
                    const m = kl(o, i, u);
                    r[u] ? r[u].p(m, n) : (r[u] = El(),
                    r[u].c(),
                    r[u].m(l, null))
                }
                for (; u < r.length; u += 1)
                    r[u].d(1);
                r.length = i.length
            }
            n & 64 && te(e, "--icon", "url(" + ((c = (f = o[15]) == null ? void 0 : f.Icon) == null ? void 0 : c.replace("ef/", "ef/skillicon/")) + ")"),
            n & 96 && a !== (a = o[16]) && d(e, "data-level", a)
        },
        d(o) {
            o && h(e),
            Pe(r, o)
        }
    }
}
function cs(s) {
    let e, l, t, a, i;
    return {
        c() {
            e = b("div"),
            l = b("div"),
            a = H(),
            this.h()
        },
        l(r) {
            e = k(r, "DIV", {
                class: !0,
                style: !0,
                "data-level": !0
            });
            var o = E(e);
            l = k(o, "DIV", {
                class: !0,
                "data-level": !0
            }),
            E(l).forEach(h),
            a = R(o),
            o.forEach(h),
            this.h()
        },
        h() {
            var r;
            d(l, "class", "upg svelte-mpem34"),
            d(l, "data-level", t = s[16]),
            d(e, "class", "FactorySkill svelte-mpem34"),
            te(e, "--icon", "url(" + ((r = s[15]) == null ? void 0 : r.Icon) + ")"),
            d(e, "data-level", i = s[16])
        },
        m(r, o) {
            M(r, e, o),
            g(e, l),
            g(e, a)
        },
        p(r, o) {
            var n;
            o & 96 && t !== (t = r[16]) && d(l, "data-level", t),
            o & 64 && te(e, "--icon", "url(" + ((n = r[15]) == null ? void 0 : n.Icon) + ")"),
            o & 96 && i !== (i = r[16]) && d(e, "data-level", i)
        },
        d(r) {
            r && h(e)
        }
    }
}
function El(s) {
    let e;
    return {
        c() {
            e = b("i"),
            this.h()
        },
        l(l) {
            e = k(l, "I", {
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "svelte-mpem34")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function wl(s) {
    let e;
    function l(i, r) {
        return i[15].Type == Ta.Factory ? cs : os
    }
    let t = l(s)
      , a = t(s);
    return {
        c() {
            a.c(),
            e = Oe()
        },
        l(i) {
            a.l(i),
            e = Oe()
        },
        m(i, r) {
            a.m(i, r),
            M(i, e, r)
        },
        p(i, r) {
            t === (t = l(i)) && a ? a.p(i, r) : (a.d(1),
            a = t(i),
            a && (a.c(),
            a.m(e.parentNode, e)))
        },
        d(i) {
            i && h(e),
            a.d(i)
        }
    }
}
function fs(s) {
    let e, l, t, a;
    const i = [is, ss]
      , r = [];
    function o(n, f) {
        return n[1] ? 0 : 1
    }
    return l = o(s),
    t = r[l] = i[l](s),
    {
        c() {
            e = b("div"),
            t.c(),
            this.h()
        },
        l(n) {
            e = k(n, "DIV", {
                class: !0
            });
            var f = E(e);
            t.l(f),
            f.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "Skills svelte-mpem34")
        },
        m(n, f) {
            M(n, e, f),
            r[l].m(e, null),
            a = !0
        },
        p(n, [f]) {
            let c = l;
            l = o(n),
            l === c ? r[l].p(n, f) : (me(),
            y(r[c], 1, 1, () => {
                r[c] = null
            }
            ),
            de(),
            t = r[l],
            t ? t.p(n, f) : (t = r[l] = i[l](n),
            t.c()),
            I(t, 1),
            t.m(e, null))
        },
        i(n) {
            a || (I(t),
            a = !0)
        },
        o(n) {
            y(t),
            a = !1
        },
        d(n) {
            n && h(e),
            r[l].d()
        }
    }
}
function us(s, e, l) {
    let t, a, i, r, o, n, {avatar: f} = e, {ship: c=!1} = e, {skillProps: u=void 0} = e;
    function m(w) {
        const _ = {};
        for (var [V,T] of t)
            _[T.Index] || (_[T.Index] = 0),
            f.data.talent.latestFactorySkillNodes.includes(V) && (_[T.Index] = T.Level),
            f.data.talent.latestPassiveSkillNodes.includes(V) && (_[T.Index] = T.Level);
        return _
    }
    function A(w) {
        const _ = {}
          , V = f.meta.excel.AttributeNodes
          , T = Object.values(V)[0]
          , N = Object.keys(T)[0];
        _[N] = 0,
        f.data.talent.attrNodes.forEach(x => {
            for (var $ in f.meta.excel.AttributeNodes[x])
                _[$] || (_[$] = 0),
                _[$] += f.meta.excel.AttributeNodes[x][$]
        }
        );
        const G = Object.keys(_)[0]
          , ae = _[G];
        return new q(G,ae)
    }
    const P = at("highlight");
    ve(s, P, w => l(9, n = w));
    const p = () => r.value ? q.mouseleave(P, r) : ""
      , D = () => r.value ? q.mouseenter(P, r) : "";
    return s.$$set = w => {
        "avatar"in w && l(0, f = w.avatar),
        "ship"in w && l(1, c = w.ship),
        "skillProps"in w && l(2, u = w.skillProps)
    }
    ,
    s.$$.update = () => {
        s.$$.dirty & 1 && l(8, t = Object.entries(f.meta.excel.NodeSkillMap).sort( (w, _) => w[1].Index - _[1].Index)),
        s.$$.dirty & 256 && l(6, a = t.filter( (w, _) => w[1].Level == 1)),
        s.$$.dirty & 1 && l(5, i = m()),
        s.$$.dirty & 1 && l(3, r = A()),
        s.$$.dirty & 520 && l(4, o = n.includes(r.simpleName) && !n.includes("Atk"))
    }
    ,
    [f, c, u, r, o, i, a, P, t, n, p, D]
}
class da extends Ye {
    constructor(e) {
        super(),
        Je(this, e, us, fs, Qe, {
            avatar: 0,
            ship: 1,
            skillProps: 2
        })
    }
}
function yl(s, e, l) {
    const t = s.slice();
    return t[7] = e[l],
    t[9] = l,
    t
}
function Cl(s, e, l) {
    const t = s.slice();
    return t[7] = e[l],
    t[9] = l,
    t
}
function Pl(s) {
    let e, l;
    return e = new St({
        props: {
            prop: s[7],
            type: "attr"
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a & 2 && (i.prop = t[7]),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function Nl(s) {
    let e, l;
    return e = new St({
        props: {
            prop: s[7],
            type: "full"
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a & 2 && (i.prop = t[7]),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function hs(s) {
    let e, l, t, a, i, r, o, n, f = ee(s[1].slice(0, 4)), c = [];
    for (let p = 0; p < f.length; p += 1)
        c[p] = Pl(Cl(s, f, p));
    const u = p => y(c[p], 1, 1, () => {
        c[p] = null
    }
    );
    let m = ee(s[1].slice(4))
      , A = [];
    for (let p = 0; p < m.length; p += 1)
        A[p] = Nl(yl(s, m, p));
    const P = p => y(A[p], 1, 1, () => {
        A[p] = null
    }
    );
    return o = new da({
        props: {
            avatar: s[0],
            skillProps: s[2]
        }
    }),
    {
        c() {
            e = b("div"),
            l = b("div"),
            t = H(),
            a = b("div");
            for (let p = 0; p < c.length; p += 1)
                c[p].c();
            i = H();
            for (let p = 0; p < A.length; p += 1)
                A[p].c();
            r = H(),
            j(o.$$.fragment),
            this.h()
        },
        l(p) {
            e = k(p, "DIV", {
                class: !0
            });
            var D = E(e);
            l = k(D, "DIV", {
                class: !0,
                style: !0
            }),
            E(l).forEach(h),
            t = R(D),
            a = k(D, "DIV", {
                class: !0
            });
            var w = E(a);
            for (let _ = 0; _ < c.length; _ += 1)
                c[_].l(w);
            w.forEach(h),
            i = R(D);
            for (let _ = 0; _ < A.length; _ += 1)
                A[_].l(D);
            r = R(D),
            K(o.$$.fragment, D),
            D.forEach(h),
            this.h()
        },
        h() {
            d(l, "class", "head svelte-hz29tp"),
            te(l, "--image", "url(" + s[0].flavorImage + ")"),
            d(a, "class", "attrs svelte-hz29tp"),
            d(e, "class", "Stats svelte-hz29tp")
        },
        m(p, D) {
            M(p, e, D),
            g(e, l),
            g(e, t),
            g(e, a);
            for (let w = 0; w < c.length; w += 1)
                c[w] && c[w].m(a, null);
            g(e, i);
            for (let w = 0; w < A.length; w += 1)
                A[w] && A[w].m(e, null);
            g(e, r),
            Q(o, e, null),
            n = !0
        },
        p(p, [D]) {
            if ((!n || D & 1) && te(l, "--image", "url(" + p[0].flavorImage + ")"),
            D & 2) {
                f = ee(p[1].slice(0, 4));
                let _;
                for (_ = 0; _ < f.length; _ += 1) {
                    const V = Cl(p, f, _);
                    c[_] ? (c[_].p(V, D),
                    I(c[_], 1)) : (c[_] = Pl(V),
                    c[_].c(),
                    I(c[_], 1),
                    c[_].m(a, null))
                }
                for (me(),
                _ = f.length; _ < c.length; _ += 1)
                    u(_);
                de()
            }
            if (D & 2) {
                m = ee(p[1].slice(4));
                let _;
                for (_ = 0; _ < m.length; _ += 1) {
                    const V = yl(p, m, _);
                    A[_] ? (A[_].p(V, D),
                    I(A[_], 1)) : (A[_] = Nl(V),
                    A[_].c(),
                    I(A[_], 1),
                    A[_].m(e, r))
                }
                for (me(),
                _ = m.length; _ < A.length; _ += 1)
                    P(_);
                de()
            }
            const w = {};
            D & 1 && (w.avatar = p[0]),
            D & 4 && (w.skillProps = p[2]),
            o.$set(w)
        },
        i(p) {
            if (!n) {
                for (let D = 0; D < f.length; D += 1)
                    I(c[D]);
                for (let D = 0; D < m.length; D += 1)
                    I(A[D]);
                I(o.$$.fragment, p),
                n = !0
            }
        },
        o(p) {
            c = c.filter(Boolean);
            for (let D = 0; D < c.length; D += 1)
                y(c[D]);
            A = A.filter(Boolean);
            for (let D = 0; D < A.length; D += 1)
                y(A[D]);
            y(o.$$.fragment, p),
            n = !1
        },
        d(p) {
            p && h(e),
            Pe(c, p),
            Pe(A, p),
            Y(o)
        }
    }
}
function _s(s, e, l) {
    let {avatar: t} = e, a = !0, i, r = [], o;
    function n() {
        i = new xa,
        i.add(tt.avatar(t)),
        i.add(tt.pots(t)),
        i.add(tt.weapon(t.weapon)),
        i.add(tt.weaponAffixes(t, t.weapon)),
        i.add(tt.equips(Object.values(t.relics), t)),
        i.add(tt.equipSuit(Object.values(t.relics))),
        i.add(tt.skills(t)),
        i.add(tt.attributeConversion(i)),
        i.add(tt.attributeAtkConversion(t, i)),
        i.add(tt.corrections(t, i));
        const f = i.sum().props
          , c = new Set([J.NormalAttackDamageIncrease_base, J.NormalSkillDamageIncrease_base, J.ComboSkillDamageIncrease_base, J.UltimateSkillDamageIncrease_base]);
        l(1, r = f.filter(u => {
            if (u.value <= 0 || c.has(u.id))
                return !1;
            const m = t.meta.element;
            return !(u.simpleName.includes("GainScalar") && u.value < 1.000001 || u.isElement && !u.simpleName.includes(m))
        }
        )),
        i.sum("avatar", "pots", "weapon", "attributeConversion").props,
        l(2, o = f.filter(u => c.has(u.id)))
    }
    return ha( () => {
        l(3, a = !0)
    }
    ),
    s.$$set = f => {
        "avatar"in f && l(0, t = f.avatar)
    }
    ,
    s.$$.update = () => {
        s.$$.dirty & 9 && t && a && n()
    }
    ,
    [t, r, o, a]
}
class ms extends Ye {
    constructor(e) {
        super(),
        Je(this, e, _s, hs, Qe, {
            avatar: 0
        })
    }
}
function Vl(s, e, l) {
    const t = s.slice();
    return t[1] = e[l],
    t
}
function Tl(s) {
    let e, l;
    return e = new Mt({
        props: {
            name: "Star"
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p: be,
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function ds(s) {
    let e, l, t = ee({
        length: s[0]
    }), a = [];
    for (let r = 0; r < t.length; r += 1)
        a[r] = Tl(Vl(s, t, r));
    const i = r => y(a[r], 1, 1, () => {
        a[r] = null
    }
    );
    return {
        c() {
            e = b("div");
            for (let r = 0; r < a.length; r += 1)
                a[r].c();
            this.h()
        },
        l(r) {
            e = k(r, "DIV", {
                class: !0
            });
            var o = E(e);
            for (let n = 0; n < a.length; n += 1)
                a[n].l(o);
            o.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "rarity svelte-ahy1vd")
        },
        m(r, o) {
            M(r, e, o);
            for (let n = 0; n < a.length; n += 1)
                a[n] && a[n].m(e, null);
            l = !0
        },
        p(r, [o]) {
            if (o & 1) {
                t = ee({
                    length: r[0]
                });
                let n;
                for (n = 0; n < t.length; n += 1) {
                    const f = Vl(r, t, n);
                    a[n] ? (a[n].p(f, o),
                    I(a[n], 1)) : (a[n] = Tl(),
                    a[n].c(),
                    I(a[n], 1),
                    a[n].m(e, null))
                }
                for (me(),
                n = t.length; n < a.length; n += 1)
                    i(n);
                de()
            }
        },
        i(r) {
            if (!l) {
                for (let o = 0; o < t.length; o += 1)
                    I(a[o]);
                l = !0
            }
        },
        o(r) {
            a = a.filter(Boolean);
            for (let o = 0; o < a.length; o += 1)
                y(a[o]);
            l = !1
        },
        d(r) {
            r && h(e),
            Pe(a, r)
        }
    }
}
function gs(s, e, l) {
    let {rarity: t=0} = e;
    return s.$$set = a => {
        "rarity"in a && l(0, t = a.rarity)
    }
    ,
    [t]
}
class ga extends Ye {
    constructor(e) {
        super(),
        Je(this, e, gs, ds, Qe, {
            rarity: 0
        })
    }
}
function ps(s) {
    let e, l, t;
    return l = new Mt({
        props: {
            name: "Pot"
        }
    }),
    {
        c() {
            e = b("div"),
            j(l.$$.fragment),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0,
                "data-level": !0
            });
            var i = E(e);
            K(l.$$.fragment, i),
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "Pot svelte-p42kmn"),
            d(e, "data-level", s[0]),
            z(e, "shade", s[1])
        },
        m(a, i) {
            M(a, e, i),
            Q(l, e, null),
            t = !0
        },
        p(a, [i]) {
            (!t || i & 1) && d(e, "data-level", a[0]),
            (!t || i & 2) && z(e, "shade", a[1])
        },
        i(a) {
            t || (I(l.$$.fragment, a),
            t = !0)
        },
        o(a) {
            y(l.$$.fragment, a),
            t = !1
        },
        d(a) {
            a && h(e),
            Y(l)
        }
    }
}
function vs(s, e, l) {
    let {level: t=0} = e
      , {shade: a=!0} = e;
    return s.$$set = i => {
        "level"in i && l(0, t = i.level),
        "shade"in i && l(1, a = i.shade)
    }
    ,
    [t, a]
}
class pa extends Ye {
    constructor(e) {
        super(),
        Je(this, e, vs, ps, Qe, {
            level: 0,
            shade: 1
        })
    }
}
function Ml(s, e, l) {
    const t = s.slice();
    return t[6] = e[l],
    t
}
function Hl(s, e, l) {
    const t = s.slice();
    return t[9] = e[l],
    t
}
function Rl(s, e, l) {
    const t = s.slice();
    return t[12] = e[l],
    t
}
function Ll(s, e, l) {
    const t = s.slice();
    return t[12] = e[l],
    t
}
function Fl(s, e, l) {
    const t = s.slice();
    return t[12] = e[l],
    t
}
function Bl(s, e, l) {
    const t = s.slice();
    return t[12] = e[l],
    t
}
function bs(s) {
    const e = s.slice()
      , l = Ma.TemplateItems[e[2].data.attachedGem.templateId];
    return e[21] = l,
    e
}
function Gl(s) {
    let e, l, t, a, i, r, o = s[3](s[2].meta.nameHash) + "", n, f, c, u, m, A, P, p, D, w = "POTENTIAL", _, V, T, N = s[2].level + "", G, ae, x = s[2].ascension * 20 + (s[2].ascension > 3 ? 10 : 20) + "", $, O, B, L = "LEVEL", ge, fe, ke = "", C, le, ne, Ne, Ve, $e, pe;
    t = new _a({
        props: {
            url: s[2].meta.image,
            $$slots: {
                default: [ks, ({url: F, loaded: W}) => ({
                    22: F,
                    23: W
                }), ({url: F, loaded: W}) => (F ? 4194304 : 0) | (W ? 8388608 : 0)]
            },
            $$scope: {
                ctx: s
            }
        }
    });
    function Be(F, W) {
        return F[2].data.attachedGem ? Ul : Is
    }
    function ie(F, W) {
        return W === Ul ? bs(F) : F
    }
    let oe = Be(s)
      , re = oe(ie(s, oe));
    c = new ga({
        props: {
            rarity: s[2].meta.rarity
        }
    }),
    P = new pa({
        props: {
            shade: !1,
            level: s[2].refine
        }
    }),
    Ne = new St({
        props: {
            type: "base",
            prop: s[1].baseAtk
        }
    });
    let ue = ee(s[1].skillStats)
      , X = [];
    for (let F = 0; F < ue.length; F += 1)
        X[F] = Kl(Ml(s, ue, F));
    const st = F => y(X[F], 1, 1, () => {
        X[F] = null
    }
    );
    return {
        c() {
            e = b("div"),
            l = b("div"),
            j(t.$$.fragment),
            a = H(),
            re.c(),
            i = H(),
            r = b("div"),
            n = De(o),
            f = H(),
            j(c.$$.fragment),
            u = H(),
            m = b("div"),
            A = b("div"),
            j(P.$$.fragment),
            p = H(),
            D = b("i"),
            D.textContent = w,
            _ = H(),
            V = b("div"),
            T = b("span"),
            G = De(N),
            ae = De(`
					/`),
            $ = De(x),
            O = H(),
            B = b("i"),
            B.textContent = L,
            ge = H(),
            fe = b("div"),
            fe.innerHTML = ke,
            C = H(),
            le = b("div"),
            ne = b("div"),
            j(Ne.$$.fragment),
            Ve = H(),
            $e = b("div");
            for (let F = 0; F < X.length; F += 1)
                X[F].c();
            this.h()
        },
        l(F) {
            e = k(F, "DIV", {
                class: !0,
                style: !0
            });
            var W = E(e);
            l = k(W, "DIV", {
                class: !0
            });
            var se = E(l);
            K(t.$$.fragment, se),
            a = R(se),
            re.l(se),
            i = R(se),
            r = k(se, "DIV", {
                class: !0
            });
            var Ae = E(r);
            n = Se(Ae, o),
            Ae.forEach(h),
            f = R(se),
            K(c.$$.fragment, se),
            u = R(se),
            m = k(se, "DIV", {
                class: !0
            });
            var ce = E(m);
            A = k(ce, "DIV", {
                class: !0
            });
            var he = E(A);
            K(P.$$.fragment, he),
            p = R(he),
            D = k(he, "I", {
                class: !0,
                "data-svelte-h": !0
            }),
            Dt(D) !== "svelte-17on9n8" && (D.textContent = w),
            he.forEach(h),
            _ = R(ce),
            V = k(ce, "DIV", {
                class: !0
            });
            var Z = E(V);
            T = k(Z, "SPAN", {
                class: !0
            });
            var Re = E(T);
            G = Se(Re, N),
            Re.forEach(h),
            ae = Se(Z, `
					/`),
            $ = Se(Z, x),
            O = R(Z),
            B = k(Z, "I", {
                class: !0,
                "data-svelte-h": !0
            }),
            Dt(B) !== "svelte-1h108jg" && (B.textContent = L),
            Z.forEach(h),
            ce.forEach(h),
            se.forEach(h),
            ge = R(W),
            fe = k(W, "DIV", {
                class: !0,
                "data-svelte-h": !0
            }),
            Dt(fe) !== "svelte-1r4gsrh" && (fe.innerHTML = ke),
            C = R(W),
            le = k(W, "DIV", {
                class: !0
            });
            var Te = E(le);
            ne = k(Te, "DIV", {
                class: !0
            });
            var ot = E(ne);
            K(Ne.$$.fragment, ot),
            ot.forEach(h),
            Ve = R(Te),
            $e = k(Te, "DIV", {
                class: !0
            });
            var Ie = E($e);
            for (let Ee = 0; Ee < X.length; Ee += 1)
                X[Ee].l(Ie);
            Ie.forEach(h),
            Te.forEach(h),
            W.forEach(h),
            this.h()
        },
        h() {
            d(r, "class", "name svelte-hl4ok0"),
            d(D, "class", "svelte-hl4ok0"),
            d(A, "class", "refine svelte-hl4ok0"),
            d(T, "class", "svelte-hl4ok0"),
            d(B, "class", "svelte-hl4ok0"),
            d(V, "class", "level efnum svelte-hl4ok0"),
            d(m, "class", "prog svelte-hl4ok0"),
            d(l, "class", "desc svelte-hl4ok0"),
            d(fe, "class", "stats svelte-hl4ok0"),
            d(ne, "class", "base svelte-hl4ok0"),
            z(ne, "shift", !s[2].data.attachedGem),
            d($e, "class", "passives svelte-hl4ok0"),
            d(le, "class", "attributes svelte-hl4ok0"),
            d(e, "class", "Weapon svelte-hl4ok0"),
            te(e, "--rarityColor", Tt.Rarities[s[2].meta.rarity].color)
        },
        m(F, W) {
            M(F, e, W),
            g(e, l),
            Q(t, l, null),
            g(l, a),
            re.m(l, null),
            g(l, i),
            g(l, r),
            g(r, n),
            g(l, f),
            Q(c, l, null),
            g(l, u),
            g(l, m),
            g(m, A),
            Q(P, A, null),
            g(A, p),
            g(A, D),
            g(m, _),
            g(m, V),
            g(V, T),
            g(T, G),
            g(V, ae),
            g(V, $),
            g(V, O),
            g(V, B),
            g(e, ge),
            g(e, fe),
            g(e, C),
            g(e, le),
            g(le, ne),
            Q(Ne, ne, null),
            g(le, Ve),
            g(le, $e);
            for (let se = 0; se < X.length; se += 1)
                X[se] && X[se].m($e, null);
            pe = !0
        },
        p(F, W) {
            const se = {};
            W & 4 && (se.url = F[2].meta.image),
            W & 29360132 && (se.$$scope = {
                dirty: W,
                ctx: F
            }),
            t.$set(se),
            oe === (oe = Be(F)) && re ? re.p(ie(F, oe), W) : (re.d(1),
            re = oe(ie(F, oe)),
            re && (re.c(),
            re.m(l, i))),
            (!pe || W & 12) && o !== (o = F[3](F[2].meta.nameHash) + "") && Fe(n, o);
            const Ae = {};
            W & 4 && (Ae.rarity = F[2].meta.rarity),
            c.$set(Ae);
            const ce = {};
            W & 4 && (ce.level = F[2].refine),
            P.$set(ce),
            (!pe || W & 4) && N !== (N = F[2].level + "") && Fe(G, N),
            (!pe || W & 4) && x !== (x = F[2].ascension * 20 + (F[2].ascension > 3 ? 10 : 20) + "") && Fe($, x);
            const he = {};
            if (W & 2 && (he.prop = F[1].baseAtk),
            Ne.$set(he),
            (!pe || W & 4) && z(ne, "shift", !F[2].data.attachedGem),
            W & 3) {
                ue = ee(F[1].skillStats);
                let Z;
                for (Z = 0; Z < ue.length; Z += 1) {
                    const Re = Ml(F, ue, Z);
                    X[Z] ? (X[Z].p(Re, W),
                    I(X[Z], 1)) : (X[Z] = Kl(Re),
                    X[Z].c(),
                    I(X[Z], 1),
                    X[Z].m($e, null))
                }
                for (me(),
                Z = ue.length; Z < X.length; Z += 1)
                    st(Z);
                de()
            }
            (!pe || W & 4) && te(e, "--rarityColor", Tt.Rarities[F[2].meta.rarity].color)
        },
        i(F) {
            if (!pe) {
                I(t.$$.fragment, F),
                I(c.$$.fragment, F),
                I(P.$$.fragment, F),
                I(Ne.$$.fragment, F);
                for (let W = 0; W < ue.length; W += 1)
                    I(X[W]);
                pe = !0
            }
        },
        o(F) {
            y(t.$$.fragment, F),
            y(c.$$.fragment, F),
            y(P.$$.fragment, F),
            y(Ne.$$.fragment, F),
            X = X.filter(Boolean);
            for (let W = 0; W < X.length; W += 1)
                y(X[W]);
            pe = !1
        },
        d(F) {
            F && h(e),
            Y(t),
            re.d(),
            Y(c),
            Y(P),
            Y(Ne),
            Pe(X, F)
        }
    }
}
function ks(s) {
    let e, l, t;
    return {
        c() {
            e = b("figure"),
            l = b("img"),
            this.h()
        },
        l(a) {
            e = k(a, "FIGURE", {
                class: !0
            });
            var i = E(e);
            l = k(i, "IMG", {
                src: !0,
                alt: !0,
                class: !0
            }),
            i.forEach(h),
            this.h()
        },
        h() {
            Ke(l.src, t = s[22]) || d(l, "src", t),
            d(l, "alt", ""),
            d(l, "class", "svelte-hl4ok0"),
            z(l, "flip", s[2].meta.role == "Lance" || s[2].meta.role == "Claymores" || s[2].meta.role == "Sword"),
            z(l, "shift", s[2].meta.role == "Pistol" || s[2].meta.role == "Wand"),
            d(e, "class", "svelte-hl4ok0"),
            z(e, "loader", !s[23])
        },
        m(a, i) {
            M(a, e, i),
            g(e, l)
        },
        p(a, i) {
            i & 4194304 && !Ke(l.src, t = a[22]) && d(l, "src", t),
            i & 4 && z(l, "flip", a[2].meta.role == "Lance" || a[2].meta.role == "Claymores" || a[2].meta.role == "Sword"),
            i & 4 && z(l, "shift", a[2].meta.role == "Pistol" || a[2].meta.role == "Wand"),
            i & 8388608 && z(e, "loader", !a[23])
        },
        d(a) {
            a && h(e)
        }
    }
}
function Is(s) {
    let e;
    return {
        c() {
            e = b("div"),
            this.h()
        },
        l(l) {
            e = k(l, "DIV", {
                class: !0,
                style: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "essence svelte-hl4ok0"),
            te(e, "--icon", "url(/ui/ef/undefined.png)"),
            te(e, "--rarityColor", "transparent")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function Ul(s) {
    let e, l;
    return {
        c() {
            e = b("div"),
            l = b("div"),
            this.h()
        },
        l(t) {
            e = k(t, "DIV", {
                class: !0,
                style: !0
            });
            var a = E(e);
            l = k(a, "DIV", {
                class: !0,
                style: !0
            }),
            E(l).forEach(h),
            a.forEach(h),
            this.h()
        },
        h() {
            d(l, "class", "tag svelte-hl4ok0"),
            te(l, "--icon", "url(" + ol(s[0].data.weapon.attachedGem.terms) + ")"),
            d(e, "class", "essence svelte-hl4ok0"),
            te(e, "--icon", "url(" + s[21].Icon.replace("ef/", "ef/itemicon/") + ")"),
            te(e, "--rarityColor", Tt.Rarities[s[21].Icon.replace(/[^0-9]/g, "")].color)
        },
        m(t, a) {
            M(t, e, a),
            g(e, l)
        },
        p(t, a) {
            a & 1 && te(l, "--icon", "url(" + ol(t[0].data.weapon.attachedGem.terms) + ")"),
            a & 4 && te(e, "--icon", "url(" + t[21].Icon.replace("ef/", "ef/itemicon/") + ")"),
            a & 4 && te(e, "--rarityColor", Tt.Rarities[t[21].Icon.replace(/[^0-9]/g, "")].color)
        },
        d(t) {
            t && h(e)
        }
    }
}
function Wl(s) {
    let e;
    return {
        c() {
            e = b("i"),
            this.h()
        },
        l(l) {
            e = k(l, "I", {
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "s svelte-hl4ok0")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function Ol(s) {
    let e;
    return {
        c() {
            e = b("i"),
            this.h()
        },
        l(l) {
            e = k(l, "I", {
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "e svelte-hl4ok0")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function ql(s) {
    let e;
    return {
        c() {
            e = b("i"),
            this.h()
        },
        l(l) {
            e = k(l, "I", {
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "o svelte-hl4ok0")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function zl(s) {
    let e;
    return {
        c() {
            e = b("i"),
            this.h()
        },
        l(l) {
            e = k(l, "I", {
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "x svelte-hl4ok0")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function jl(s) {
    let e, l;
    return e = new St({
        props: {
            type: "soft",
            prop: s[9]
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a & 3 && (i.prop = t[9]),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function Kl(s) {
    var T, N, G, ae, x;
    let e, l, t, a, i, r, o, n, f = ee({
        length: (T = s[6][0]) == null ? void 0 : T.lower
    }), c = [];
    for (let $ = 0; $ < f.length; $ += 1)
        c[$] = Wl(Bl(s, f, $));
    let u = ee({
        length: (N = s[6][0]) == null ? void 0 : N.extra
    })
      , m = [];
    for (let $ = 0; $ < u.length; $ += 1)
        m[$] = Ol(Fl(s, u, $));
    let A = ee({
        length: ((G = s[6][0]) == null ? void 0 : G.upper) - ((ae = s[6][0]) == null ? void 0 : ae.total)
    })
      , P = [];
    for (let $ = 0; $ < A.length; $ += 1)
        P[$] = ql(Ll(s, A, $));
    let p = ee({
        length: 9 - ((x = s[6][0]) == null ? void 0 : x.upper)
    })
      , D = [];
    for (let $ = 0; $ < p.length; $ += 1)
        D[$] = zl(Rl(s, p, $));
    let w = ee(q.joinElements(s[6].filter(Ql).map(s[5])))
      , _ = [];
    for (let $ = 0; $ < w.length; $ += 1)
        _[$] = jl(Hl(s, w, $));
    const V = $ => y(_[$], 1, 1, () => {
        _[$] = null
    }
    );
    return {
        c() {
            e = b("div"),
            l = b("div");
            for (let $ = 0; $ < c.length; $ += 1)
                c[$].c();
            t = H();
            for (let $ = 0; $ < m.length; $ += 1)
                m[$].c();
            a = H();
            for (let $ = 0; $ < P.length; $ += 1)
                P[$].c();
            i = H();
            for (let $ = 0; $ < D.length; $ += 1)
                D[$].c();
            r = H();
            for (let $ = 0; $ < _.length; $ += 1)
                _[$].c();
            o = H(),
            this.h()
        },
        l($) {
            e = k($, "DIV", {
                class: !0
            });
            var O = E(e);
            l = k(O, "DIV", {
                class: !0
            });
            var B = E(l);
            for (let L = 0; L < c.length; L += 1)
                c[L].l(B);
            t = R(B);
            for (let L = 0; L < m.length; L += 1)
                m[L].l(B);
            a = R(B);
            for (let L = 0; L < P.length; L += 1)
                P[L].l(B);
            i = R(B);
            for (let L = 0; L < D.length; L += 1)
                D[L].l(B);
            B.forEach(h),
            r = R(O);
            for (let L = 0; L < _.length; L += 1)
                _[L].l(O);
            o = R(O),
            O.forEach(h),
            this.h()
        },
        h() {
            d(l, "class", "passive svelte-hl4ok0"),
            d(e, "class", "passive-host svelte-hl4ok0")
        },
        m($, O) {
            M($, e, O),
            g(e, l);
            for (let B = 0; B < c.length; B += 1)
                c[B] && c[B].m(l, null);
            g(l, t);
            for (let B = 0; B < m.length; B += 1)
                m[B] && m[B].m(l, null);
            g(l, a);
            for (let B = 0; B < P.length; B += 1)
                P[B] && P[B].m(l, null);
            g(l, i);
            for (let B = 0; B < D.length; B += 1)
                D[B] && D[B].m(l, null);
            g(e, r);
            for (let B = 0; B < _.length; B += 1)
                _[B] && _[B].m(e, null);
            g(e, o),
            n = !0
        },
        p($, O) {
            var B, L, ge, fe, ke;
            if (O & 2) {
                f = ee({
                    length: (B = $[6][0]) == null ? void 0 : B.lower
                });
                let C;
                for (C = 0; C < f.length; C += 1) {
                    const le = Bl($, f, C);
                    c[C] ? c[C].p(le, O) : (c[C] = Wl(),
                    c[C].c(),
                    c[C].m(l, t))
                }
                for (; C < c.length; C += 1)
                    c[C].d(1);
                c.length = f.length
            }
            if (O & 2) {
                u = ee({
                    length: (L = $[6][0]) == null ? void 0 : L.extra
                });
                let C;
                for (C = 0; C < u.length; C += 1) {
                    const le = Fl($, u, C);
                    m[C] ? m[C].p(le, O) : (m[C] = Ol(),
                    m[C].c(),
                    m[C].m(l, a))
                }
                for (; C < m.length; C += 1)
                    m[C].d(1);
                m.length = u.length
            }
            if (O & 2) {
                A = ee({
                    length: ((ge = $[6][0]) == null ? void 0 : ge.upper) - ((fe = $[6][0]) == null ? void 0 : fe.total)
                });
                let C;
                for (C = 0; C < A.length; C += 1) {
                    const le = Ll($, A, C);
                    P[C] ? P[C].p(le, O) : (P[C] = ql(),
                    P[C].c(),
                    P[C].m(l, i))
                }
                for (; C < P.length; C += 1)
                    P[C].d(1);
                P.length = A.length
            }
            if (O & 2) {
                p = ee({
                    length: 9 - ((ke = $[6][0]) == null ? void 0 : ke.upper)
                });
                let C;
                for (C = 0; C < p.length; C += 1) {
                    const le = Rl($, p, C);
                    D[C] ? D[C].p(le, O) : (D[C] = zl(),
                    D[C].c(),
                    D[C].m(l, null))
                }
                for (; C < D.length; C += 1)
                    D[C].d(1);
                D.length = p.length
            }
            if (O & 3) {
                w = ee(q.joinElements($[6].filter(Ql).map($[5])));
                let C;
                for (C = 0; C < w.length; C += 1) {
                    const le = Hl($, w, C);
                    _[C] ? (_[C].p(le, O),
                    I(_[C], 1)) : (_[C] = jl(le),
                    _[C].c(),
                    I(_[C], 1),
                    _[C].m(e, o))
                }
                for (me(),
                C = w.length; C < _.length; C += 1)
                    V(C);
                de()
            }
        },
        i($) {
            if (!n) {
                for (let O = 0; O < w.length; O += 1)
                    I(_[O]);
                n = !0
            }
        },
        o($) {
            _ = _.filter(Boolean);
            for (let O = 0; O < _.length; O += 1)
                y(_[O]);
            n = !1
        },
        d($) {
            $ && h(e),
            Pe(c, $),
            Pe(m, $),
            Pe(P, $),
            Pe(D, $),
            Pe(_, $)
        }
    }
}
function Ds(s) {
    let e, l, t = s[2] && Gl(s);
    return {
        c() {
            t && t.c(),
            e = Oe()
        },
        l(a) {
            t && t.l(a),
            e = Oe()
        },
        m(a, i) {
            t && t.m(a, i),
            M(a, e, i),
            l = !0
        },
        p(a, [i]) {
            a[2] ? t ? (t.p(a, i),
            i & 4 && I(t, 1)) : (t = Gl(a),
            t.c(),
            I(t, 1),
            t.m(e.parentNode, e)) : t && (me(),
            y(t, 1, 1, () => {
                t = null
            }
            ),
            de())
        },
        i(a) {
            l || (I(t),
            l = !0)
        },
        o(a) {
            y(t),
            l = !1
        },
        d(a) {
            a && h(e),
            t && t.d(a)
        }
    }
}
const Ql = s => s.prop;
function Ss(s, e, l) {
    let t, a;
    const {ef: i} = at("l10n");
    ve(s, i, f => l(3, a = f));
    let {avatar: r} = e
      , o = null;
    const n = f => new q(f.prop.convert(r),f.prop.value).remake(f.formula);
    return s.$$set = f => {
        "avatar"in f && l(0, r = f.avatar)
    }
    ,
    s.$$.update = () => {
        s.$$.dirty & 1 && l(2, t = r.weapon),
        s.$$.dirty & 5 && t && l(1, o = r.weapon.stats()),
        s.$$.dirty & 6 && console.log(t, o)
    }
    ,
    [r, o, t, a, i, n]
}
class $s extends Ye {
    constructor(e) {
        super(),
        Je(this, e, Ss, Ds, Qe, {
            avatar: 0
        })
    }
}
function As(s) {
    let e, l, t;
    return l = new Mt({
        props: {
            name: "Elite"
        }
    }),
    {
        c() {
            e = b("div"),
            j(l.$$.fragment),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0,
                "data-level": !0
            });
            var i = E(e);
            K(l.$$.fragment, i),
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "Elite svelte-1ei4ok9"),
            d(e, "data-level", s[0])
        },
        m(a, i) {
            M(a, e, i),
            Q(l, e, null),
            t = !0
        },
        p(a, [i]) {
            (!t || i & 1) && d(e, "data-level", a[0])
        },
        i(a) {
            t || (I(l.$$.fragment, a),
            t = !0)
        },
        o(a) {
            y(l.$$.fragment, a),
            t = !1
        },
        d(a) {
            a && h(e),
            Y(l)
        }
    }
}
function Es(s, e, l) {
    let {level: t=0} = e;
    return s.$$set = a => {
        "level"in a && l(0, t = a.level)
    }
    ,
    [t]
}
class ws extends Ye {
    constructor(e) {
        super(),
        Je(this, e, Es, As, Qe, {
            level: 0
        })
    }
}
function ll(s) {
    const e = s.slice()
      , l = e[1][0];
    return e[4] = l,
    e
}
function Yl(s, e, l) {
    const t = s.slice();
    return t[5] = e[l],
    t
}
function Jl(s, e, l) {
    var r;
    const t = s.slice();
    t[11] = e[l],
    t[15] = l;
    const a = ((r = t[5].data.enhance.find(function(...n) {
        return s[2](t[15], ...n)
    })) == null ? void 0 : r.value) || 0;
    t[12] = a;
    const i = new q(t[11].convert(t[0]),t[11].value);
    return t[13] = i,
    t
}
function Xl(s, e, l) {
    const t = s.slice();
    return t[16] = e[l],
    t
}
function al(s) {
    const e = s.slice()
      , l = e[5].stats();
    e[8] = l;
    const t = q.joinElements(e[8].slice(1));
    e[9] = t;
    const a = Ts(e[9]);
    return e[10] = a,
    e
}
function Zl(s) {
    let e, l, t, a = ee(s[0].relics), i = [];
    for (let n = 0; n < a.length; n += 1)
        i[n] = la(Yl(s, a, n));
    const r = n => y(i[n], 1, 1, () => {
        i[n] = null
    }
    );
    let o = s[1] && aa(ll(s));
    return {
        c() {
            e = b("div");
            for (let n = 0; n < i.length; n += 1)
                i[n].c();
            l = H(),
            o && o.c(),
            this.h()
        },
        l(n) {
            e = k(n, "DIV", {
                class: !0
            });
            var f = E(e);
            for (let c = 0; c < i.length; c += 1)
                i[c].l(f);
            l = R(f),
            o && o.l(f),
            f.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "Gears svelte-bqioka")
        },
        m(n, f) {
            M(n, e, f);
            for (let c = 0; c < i.length; c += 1)
                i[c] && i[c].m(e, null);
            g(e, l),
            o && o.m(e, null),
            t = !0
        },
        p(n, f) {
            if (f & 1572865) {
                a = ee(n[0].relics);
                let c;
                for (c = 0; c < a.length; c += 1) {
                    const u = Yl(n, a, c);
                    i[c] ? (i[c].p(u, f),
                    I(i[c], 1)) : (i[c] = la(u),
                    i[c].c(),
                    I(i[c], 1),
                    i[c].m(e, l))
                }
                for (me(),
                c = a.length; c < i.length; c += 1)
                    r(c);
                de()
            }
            n[1] ? o ? o.p(ll(n), f) : (o = aa(ll(n)),
            o.c(),
            o.m(e, null)) : o && (o.d(1),
            o = null)
        },
        i(n) {
            if (!t) {
                for (let f = 0; f < a.length; f += 1)
                    I(i[f]);
                t = !0
            }
        },
        o(n) {
            i = i.filter(Boolean);
            for (let f = 0; f < i.length; f += 1)
                y(i[f]);
            t = !1
        },
        d(n) {
            n && h(e),
            Pe(i, n),
            o && o.d()
        }
    }
}
function xl(s) {
    let e, l, t, a, i, r, o;
    e = new _a({
        props: {
            url: s[5].meta.image.replace("akef/", "ef/itemicon/"),
            $$slots: {
                default: [Ps, ({url: u, loaded: m}) => ({
                    19: u,
                    20: m
                }), ({url: u, loaded: m}) => (u ? 524288 : 0) | (m ? 1048576 : 0)]
            },
            $$scope: {
                ctx: s
            }
        }
    }),
    a = new St({
        props: {
            prop: s[8][0],
            type: "primary",
            plus: !0
        }
    });
    let n = ee(s[9])
      , f = [];
    for (let u = 0; u < n.length; u += 1)
        f[u] = ta(Jl(s, n, u));
    const c = u => y(f[u], 1, 1, () => {
        f[u] = null
    }
    );
    return {
        c() {
            j(e.$$.fragment),
            l = H(),
            t = b("div"),
            j(a.$$.fragment),
            i = H(),
            r = b("div");
            for (let u = 0; u < f.length; u += 1)
                f[u].c();
            this.h()
        },
        l(u) {
            K(e.$$.fragment, u),
            l = R(u),
            t = k(u, "DIV", {
                class: !0
            });
            var m = E(t);
            K(a.$$.fragment, m),
            m.forEach(h),
            i = R(u),
            r = k(u, "DIV", {
                class: !0
            });
            var A = E(r);
            for (let P = 0; P < f.length; P += 1)
                f[P].l(A);
            A.forEach(h),
            this.h()
        },
        h() {
            d(t, "class", "main svelte-bqioka"),
            d(r, "class", "subs svelte-bqioka")
        },
        m(u, m) {
            Q(e, u, m),
            M(u, l, m),
            M(u, t, m),
            Q(a, t, null),
            M(u, i, m),
            M(u, r, m);
            for (let A = 0; A < f.length; A += 1)
                f[A] && f[A].m(r, null);
            o = !0
        },
        p(u, m) {
            const A = {};
            m & 1 && (A.url = u[5].meta.image.replace("akef/", "ef/itemicon/")),
            m & 3670017 && (A.$$scope = {
                dirty: m,
                ctx: u
            }),
            e.$set(A);
            const P = {};
            if (m & 1 && (P.prop = u[8][0]),
            a.$set(P),
            m & 1) {
                n = ee(u[9]);
                let p;
                for (p = 0; p < n.length; p += 1) {
                    const D = Jl(u, n, p);
                    f[p] ? (f[p].p(D, m),
                    I(f[p], 1)) : (f[p] = ta(D),
                    f[p].c(),
                    I(f[p], 1),
                    f[p].m(r, null))
                }
                for (me(),
                p = n.length; p < f.length; p += 1)
                    c(p);
                de()
            }
        },
        i(u) {
            if (!o) {
                I(e.$$.fragment, u),
                I(a.$$.fragment, u);
                for (let m = 0; m < n.length; m += 1)
                    I(f[m]);
                o = !0
            }
        },
        o(u) {
            y(e.$$.fragment, u),
            y(a.$$.fragment, u),
            f = f.filter(Boolean);
            for (let m = 0; m < f.length; m += 1)
                y(f[m]);
            o = !1
        },
        d(u) {
            u && (h(l),
            h(t),
            h(i),
            h(r)),
            Y(e, u),
            Y(a),
            Pe(f, u)
        }
    }
}
function ys(s) {
    let e, l;
    return {
        c() {
            e = b("img"),
            this.h()
        },
        l(t) {
            e = k(t, "IMG", {
                src: !0,
                alt: !0,
                class: !0
            }),
            this.h()
        },
        h() {
            Ke(e.src, l = s[19]) || d(e, "src", l),
            d(e, "alt", ""),
            d(e, "class", "svelte-bqioka")
        },
        m(t, a) {
            M(t, e, a)
        },
        p(t, a) {
            a & 524288 && !Ke(e.src, l = t[19]) && d(e, "src", l)
        },
        i: be,
        o: be,
        d(t) {
            t && h(e)
        }
    }
}
function Cs(s) {
    let e, l;
    return e = new Ka({
        props: {
            url: s[5].meta.image.replace("akef/", "ef/itemicon/")
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a & 1 && (i.url = t[5].meta.image.replace("akef/", "ef/itemicon/")),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function Ps(s) {
    let e, l, t, a;
    const i = [Cs, ys]
      , r = [];
    function o(n, f) {
        return n[10].length ? 0 : 1
    }
    return l = o(s),
    t = r[l] = i[l](s),
    {
        c() {
            e = b("figure"),
            t.c(),
            this.h()
        },
        l(n) {
            e = k(n, "FIGURE", {});
            var f = E(e);
            t.l(f),
            f.forEach(h),
            this.h()
        },
        h() {
            z(e, "loader", !s[20])
        },
        m(n, f) {
            M(n, e, f),
            r[l].m(e, null),
            a = !0
        },
        p(n, f) {
            let c = l;
            l = o(n),
            l === c ? r[l].p(n, f) : (me(),
            y(r[c], 1, 1, () => {
                r[c] = null
            }
            ),
            de(),
            t = r[l],
            t ? t.p(n, f) : (t = r[l] = i[l](n),
            t.c()),
            I(t, 1),
            t.m(e, null)),
            (!a || f & 1048576) && z(e, "loader", !n[20])
        },
        i(n) {
            a || (I(t),
            a = !0)
        },
        o(n) {
            y(t),
            a = !1
        },
        d(n) {
            n && h(e),
            r[l].d()
        }
    }
}
function ea(s) {
    let e;
    return {
        c() {
            e = b("i"),
            this.h()
        },
        l(l) {
            e = k(l, "I", {
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "svelte-bqioka")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function Ns(s) {
    let e, l = ee({
        length: s[12]
    }), t = [];
    for (let a = 0; a < l.length; a += 1)
        t[a] = ea(Xl(s, l, a));
    return {
        c() {
            e = b("div");
            for (let a = 0; a < t.length; a += 1)
                t[a].c();
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0,
                slot: !0
            });
            var i = E(e);
            for (let r = 0; r < t.length; r += 1)
                t[r].l(i);
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "upg svelte-bqioka"),
            d(e, "slot", "postfix")
        },
        m(a, i) {
            M(a, e, i);
            for (let r = 0; r < t.length; r += 1)
                t[r] && t[r].m(e, null)
        },
        p(a, i) {
            if (i & 1) {
                l = ee({
                    length: a[12]
                });
                let r;
                for (r = 0; r < l.length; r += 1) {
                    const o = Xl(a, l, r);
                    t[r] ? t[r].p(o, i) : (t[r] = ea(),
                    t[r].c(),
                    t[r].m(e, null))
                }
                for (; r < t.length; r += 1)
                    t[r].d(1);
                t.length = l.length
            }
        },
        d(a) {
            a && h(e),
            Pe(t, a)
        }
    }
}
function ta(s) {
    let e, l;
    return e = new St({
        props: {
            prop: s[13],
            type: "soft",
            plus: !0,
            extra: s[15] == s[9].length - 1 ? s[10] : null,
            $$slots: {
                postfix: [Ns]
            },
            $$scope: {
                ctx: s
            }
        }
    }),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a & 1 && (i.prop = t[13]),
            a & 1 && (i.extra = t[15] == t[9].length - 1 ? t[10] : null),
            a & 2097153 && (i.$$scope = {
                dirty: a,
                ctx: t
            }),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function la(s) {
    let e, l, t, a, i = s[5] && xl(al(s));
    function r() {
        return s[3](s[5])
    }
    return {
        c() {
            e = b("div"),
            i && i.c(),
            this.h()
        },
        l(o) {
            e = k(o, "DIV", {
                class: !0,
                style: !0
            });
            var n = E(e);
            i && i.l(n),
            n.forEach(h),
            this.h()
        },
        h() {
            var o, n;
            d(e, "class", "Gear svelte-bqioka"),
            te(e, "--rarityColor", (n = Tt.Rarities[(o = s[5]) == null ? void 0 : o.meta.rarity]) == null ? void 0 : n.color)
        },
        m(o, n) {
            M(o, e, n),
            i && i.m(e, null),
            l = !0,
            t || (a = mt(e, "click", r),
            t = !0)
        },
        p(o, n) {
            var f, c;
            s = o,
            s[5] ? i ? (i.p(al(s), n),
            n & 1 && I(i, 1)) : (i = xl(al(s)),
            i.c(),
            I(i, 1),
            i.m(e, null)) : i && (me(),
            y(i, 1, 1, () => {
                i = null
            }
            ),
            de()),
            (!l || n & 1) && te(e, "--rarityColor", (c = Tt.Rarities[(f = s[5]) == null ? void 0 : f.meta.rarity]) == null ? void 0 : c.color)
        },
        i(o) {
            l || (I(i),
            l = !0)
        },
        o(o) {
            y(i),
            l = !1
        },
        d(o) {
            o && h(e),
            i && i.d(),
            t = !1,
            a()
        }
    }
}
function aa(s) {
    let e, l, t;
    return {
        c() {
            e = b("div"),
            l = b("img"),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0
            });
            var i = E(e);
            l = k(i, "IMG", {
                src: !0,
                class: !0
            }),
            i.forEach(h),
            this.h()
        },
        h() {
            var a;
            Ke(l.src, t = ((a = s[4]) == null ? void 0 : a.icon) || "/ui/ef/undefined.png") || d(l, "src", t),
            d(l, "class", "svelte-bqioka"),
            d(e, "class", "Set svelte-bqioka")
        },
        m(a, i) {
            M(a, e, i),
            g(e, l)
        },
        p(a, i) {
            var r;
            i & 2 && !Ke(l.src, t = ((r = a[4]) == null ? void 0 : r.icon) || "/ui/ef/undefined.png") && d(l, "src", t)
        },
        d(a) {
            a && h(e)
        }
    }
}
function Vs(s) {
    let e, l, t = s[0] && Zl(s);
    return {
        c() {
            t && t.c(),
            e = Oe()
        },
        l(a) {
            t && t.l(a),
            e = Oe()
        },
        m(a, i) {
            t && t.m(a, i),
            M(a, e, i),
            l = !0
        },
        p(a, [i]) {
            a[0] ? t ? (t.p(a, i),
            i & 1 && I(t, 1)) : (t = Zl(a),
            t.c(),
            I(t, 1),
            t.m(e.parentNode, e)) : t && (me(),
            y(t, 1, 1, () => {
                t = null
            }
            ),
            de())
        },
        i(a) {
            l || (I(t),
            l = !0)
        },
        o(a) {
            y(t),
            l = !1
        },
        d(a) {
            a && h(e),
            t && t.d(a)
        }
    }
}
function Ts(s) {
    let e;
    const l = [];
    for (var t = 1; t < s.length; t++) {
        const a = s[t];
        Math.abs((e || 0) - a.value) < 1e-4 && (l.push(a),
        s.splice(t, 1),
        t--),
        e = a.value
    }
    return l
}
function Ms(s, e, l) {
    let t, {avatar: a} = e;
    const i = (o, n) => n.key == o + 1
      , r = o => console.log(o);
    return s.$$set = o => {
        "avatar"in o && l(0, a = o.avatar)
    }
    ,
    s.$$.update = () => {
        s.$$.dirty & 1 && l(1, t = a.relicSets())
    }
    ,
    [a, t, i, r]
}
class Hs extends Ye {
    constructor(e) {
        super(),
        Je(this, e, Ms, Vs, Qe, {
            avatar: 0
        })
    }
}
function sa(s) {
    let e, l, t;
    return {
        c() {
            e = b("div"),
            l = H(),
            t = b("div"),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0
            }),
            E(e).forEach(h),
            l = R(a),
            t = k(a, "DIV", {
                class: !0
            }),
            E(t).forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "bg element svelte-pxa2i2"),
            d(t, "class", "bg shade svelte-pxa2i2")
        },
        m(a, i) {
            M(a, e, i),
            M(a, l, i),
            M(a, t, i)
        },
        d(a) {
            a && (h(e),
            h(l),
            h(t))
        }
    }
}
function Rs(s) {
    let e, l, t = {
        width: 2400,
        height: 1e3,
        DEBUG_AVID: s[0].meta.id,
        layers: s[32],
        edit: s[2]
    };
    return e = new Pa({
        props: t
    }),
    s[45](e),
    e.$on("draw", qs),
    {
        c() {
            j(e.$$.fragment)
        },
        l(a) {
            K(e.$$.fragment, a)
        },
        m(a, i) {
            Q(e, a, i),
            l = !0
        },
        p(a, i) {
            const r = {};
            i[0] & 1 && (r.DEBUG_AVID = a[0].meta.id),
            i[0] & 4 && (r.edit = a[2]),
            e.$set(r)
        },
        i(a) {
            l || (I(e.$$.fragment, a),
            l = !0)
        },
        o(a) {
            y(e.$$.fragment, a),
            l = !1
        },
        d(a) {
            s[45](null),
            Y(e, a)
        }
    }
}
function ia(s) {
    let e, l;
    return {
        c() {
            e = b("div"),
            l = De(s[19]),
            this.h()
        },
        l(t) {
            e = k(t, "DIV", {
                class: !0
            });
            var a = E(e);
            l = Se(a, s[19]),
            a.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "caption svelte-pxa2i2")
        },
        m(t, a) {
            M(t, e, a),
            g(e, l)
        },
        p(t, a) {
            a[0] & 524288 && Fe(l, t[19])
        },
        d(t) {
            t && h(e)
        }
    }
}
function Ls(s) {
    let e;
    return {
        c() {
            e = b("div"),
            this.h()
        },
        l(l) {
            e = k(l, "DIV", {
                style: !0,
                class: !0
            }),
            E(e).forEach(h),
            this.h()
        },
        h() {
            te(e, "flex-grow", "2"),
            d(e, "class", "svelte-pxa2i2")
        },
        m(l, t) {
            M(l, e, t)
        },
        p: be,
        d(l) {
            l && h(e)
        }
    }
}
function Fs(s) {
    let e, l = s[21].replace(/\./g, ".​").replace(/\//g, "/​") + "", t;
    return {
        c() {
            e = b("div"),
            t = De(l),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0,
                "data-icon": !0
            });
            var i = E(e);
            t = Se(i, l),
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "m art-source svelte-pxa2i2"),
            d(e, "data-icon", "brush")
        },
        m(a, i) {
            M(a, e, i),
            g(e, t)
        },
        p(a, i) {
            i[0] & 2097152 && l !== (l = a[21].replace(/\./g, ".​").replace(/\//g, "/​") + "") && Fe(t, l)
        },
        d(a) {
            a && h(e)
        }
    }
}
function ra(s) {
    let e, l = s[22].nickname + "", t;
    return {
        c() {
            e = b("div"),
            t = De(l),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0
            });
            var i = E(e);
            t = Se(i, l),
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "m nickname svelte-pxa2i2")
        },
        m(a, i) {
            M(a, e, i),
            g(e, t)
        },
        p(a, i) {
            i[0] & 4194304 && l !== (l = a[22].nickname + "") && Fe(t, l)
        },
        d(a) {
            a && h(e)
        }
    }
}
function na(s) {
    let e, l = s[22].uid + "", t;
    return {
        c() {
            e = b("div"),
            t = De(l),
            this.h()
        },
        l(a) {
            e = k(a, "DIV", {
                class: !0
            });
            var i = E(e);
            t = Se(i, l),
            i.forEach(h),
            this.h()
        },
        h() {
            d(e, "class", "m uid svelte-pxa2i2")
        },
        m(a, i) {
            M(a, e, i),
            g(e, t)
        },
        p(a, i) {
            i[0] & 4194304 && l !== (l = a[22].uid + "") && Fe(t, l)
        },
        d(a) {
            a && h(e)
        }
    }
}
function Bs(s) {
    let e, l;
    return e = new Ga({
        props: {
            variant: Ua.PRIMARY,
            type: Wa.FILL,
            icon: s[11] ? "loading" : "download-image"
        }
    }),
    e.$on("click", s[49]),
    {
        c() {
            j(e.$$.fragment)
        },
        l(t) {
            K(e.$$.fragment, t)
        },
        m(t, a) {
            Q(e, t, a),
            l = !0
        },
        p(t, a) {
            const i = {};
            a[0] & 2048 && (i.icon = t[11] ? "loading" : "download-image"),
            e.$set(i)
        },
        i(t) {
            l || (I(e.$$.fragment, t),
            l = !0)
        },
        o(t) {
            y(e.$$.fragment, t),
            l = !1
        },
        d(t) {
            Y(e, t)
        }
    }
}
function oa(s) {
    let e, l, t, a, i, r, o;
    function n(c) {
        s[54](c)
    }
    let f = {
        id: "0",
        labelText: s[23].app.card.adaptive_color
    };
    return s[7].adaptiveColor !== void 0 && (f.selected = s[7].adaptiveColor),
    e = new zt({
        props: f
    }),
    nt.push( () => Zt(e, "selected", n)),
    {
        c() {
            j(e.$$.fragment),
            t = H(),
            a = b("li"),
            this.h()
        },
        l(c) {
            K(e.$$.fragment, c),
            t = R(c),
            a = k(c, "LI", {
                role: !0,
                class: !0
            }),
            E(a).forEach(h),
            this.h()
        },
        h() {
            d(a, "role", "separator"),
            d(a, "class", "bx--menu-divider")
        },
        m(c, u) {
            Q(e, c, u),
            M(c, t, u),
            M(c, a, u),
            i = !0,
            r || (o = mt(a, "click", js),
            r = !0)
        },
        p(c, u) {
            const m = {};
            u[0] & 8388608 && (m.labelText = c[23].app.card.adaptive_color),
            !l && u[0] & 128 && (l = !0,
            m.selected = c[7].adaptiveColor,
            Xt( () => l = !1)),
            e.$set(m)
        },
        i(c) {
            i || (I(e.$$.fragment, c),
            i = !0)
        },
        o(c) {
            y(e.$$.fragment, c),
            i = !1
        },
        d(c) {
            c && (h(t),
            h(a)),
            Y(e, c),
            r = !1,
            o()
        }
    }
}
function ca(s) {
    let e, l, t, a, i, r;
    function o(u) {
        s[55](u)
    }
    let n = {
        id: "3",
        labelText: s[23].app.card.show_uid
    };
    s[7].uid !== void 0 && (n.selected = s[7].uid),
    e = new zt({
        props: n
    }),
    nt.push( () => Zt(e, "selected", o));
    function f(u) {
        s[56](u)
    }
    let c = {
        id: "4",
        labelText: s[23].app.card.show_username
    };
    return s[7].nickname !== void 0 && (c.selected = s[7].nickname),
    a = new zt({
        props: c
    }),
    nt.push( () => Zt(a, "selected", f)),
    {
        c() {
            j(e.$$.fragment),
            t = H(),
            j(a.$$.fragment)
        },
        l(u) {
            K(e.$$.fragment, u),
            t = R(u),
            K(a.$$.fragment, u)
        },
        m(u, m) {
            Q(e, u, m),
            M(u, t, m),
            Q(a, u, m),
            r = !0
        },
        p(u, m) {
            const A = {};
            m[0] & 8388608 && (A.labelText = u[23].app.card.show_uid),
            !l && m[0] & 128 && (l = !0,
            A.selected = u[7].uid,
            Xt( () => l = !1)),
            e.$set(A);
            const P = {};
            m[0] & 8388608 && (P.labelText = u[23].app.card.show_username),
            !i && m[0] & 128 && (i = !0,
            P.selected = u[7].nickname,
            Xt( () => i = !1)),
            a.$set(P)
        },
        i(u) {
            r || (I(e.$$.fragment, u),
            I(a.$$.fragment, u),
            r = !0)
        },
        o(u) {
            y(e.$$.fragment, u),
            y(a.$$.fragment, u),
            r = !1
        },
        d(u) {
            u && h(t),
            Y(e, u),
            Y(a, u)
        }
    }
}
function Gs(s) {
    let e, l, t, a = s[4] && oa(s), i = (s[4] || s[17]) && ca(s);
    return {
        c() {
            a && a.c(),
            e = H(),
            i && i.c(),
            l = Oe()
        },
        l(r) {
            a && a.l(r),
            e = R(r),
            i && i.l(r),
            l = Oe()
        },
        m(r, o) {
            a && a.m(r, o),
            M(r, e, o),
            i && i.m(r, o),
            M(r, l, o),
            t = !0
        },
        p(r, o) {
            r[4] ? a ? (a.p(r, o),
            o[0] & 16 && I(a, 1)) : (a = oa(r),
            a.c(),
            I(a, 1),
            a.m(e.parentNode, e)) : a && (me(),
            y(a, 1, 1, () => {
                a = null
            }
            ),
            de()),
            r[4] || r[17] ? i ? (i.p(r, o),
            o[0] & 131088 && I(i, 1)) : (i = ca(r),
            i.c(),
            I(i, 1),
            i.m(l.parentNode, l)) : i && (me(),
            y(i, 1, 1, () => {
                i = null
            }
            ),
            de())
        },
        i(r) {
            t || (I(a),
            I(i),
            t = !0)
        },
        o(r) {
            y(a),
            y(i),
            t = !1
        },
        d(r) {
            r && (h(e),
            h(l)),
            a && a.d(r),
            i && i.d(r)
        }
    }
}
function Us(s) {
    let e, l, t, a, i, r, o, n, f, c;
    return e = new zt({
        props: {
            id: "image",
            indented: !0,
            labelText: s[23].app.terms.download
        }
    }),
    e.$on("click", s[52]),
    t = new zt({
        props: {
            id: "image2",
            indented: !0,
            labelText: s[23].app.terms.download + " (2x)"
        }
    }),
    t.$on("click", s[53]),
    o = new Fa({
        props: {
            labelText: "Style options",
            $$slots: {
                default: [Gs]
            },
            $$scope: {
                ctx: s
            }
        }
    }),
    {
        c() {
            j(e.$$.fragment),
            l = H(),
            j(t.$$.fragment),
            a = H(),
            i = b("li"),
            r = H(),
            j(o.$$.fragment),
            this.h()
        },
        l(u) {
            K(e.$$.fragment, u),
            l = R(u),
            K(t.$$.fragment, u),
            a = R(u),
            i = k(u, "LI", {
                role: !0,
                class: !0
            }),
            E(i).forEach(h),
            r = R(u),
            K(o.$$.fragment, u),
            this.h()
        },
        h() {
            d(i, "role", "separator"),
            d(i, "class", "bx--menu-divider")
        },
        m(u, m) {
            Q(e, u, m),
            M(u, l, m),
            Q(t, u, m),
            M(u, a, m),
            M(u, i, m),
            M(u, r, m),
            Q(o, u, m),
            n = !0,
            f || (c = mt(i, "click", zs),
            f = !0)
        },
        p(u, m) {
            const A = {};
            m[0] & 8388608 && (A.labelText = u[23].app.terms.download),
            e.$set(A);
            const P = {};
            m[0] & 8388608 && (P.labelText = u[23].app.terms.download + " (2x)"),
            t.$set(P);
            const p = {};
            m[0] & 8519824 | m[2] & 64 && (p.$$scope = {
                dirty: m,
                ctx: u
            }),
            o.$set(p)
        },
        i(u) {
            n || (I(e.$$.fragment, u),
            I(t.$$.fragment, u),
            I(o.$$.fragment, u),
            n = !0)
        },
        o(u) {
            y(e.$$.fragment, u),
            y(t.$$.fragment, u),
            y(o.$$.fragment, u),
            n = !1
        },
        d(u) {
            u && (h(l),
            h(a),
            h(i),
            h(r)),
            Y(e, u),
            Y(t, u),
            Y(o, u),
            f = !1,
            c()
        }
    }
}
var fa;
function Ws(s) {
    let e, l, t, a = "", i, r, o = "", n, f, c, u = ".", m, A, P, p, D, w, _, V, T, N, G, ae, x, $, O, B, L, ge, fe, ke, C, le, ne, Ne, Ve, $e, pe, Be, ie, oe, re, ue, X, st, F, W, se = s[20](s[0].meta.nameHash) + "", Ae, ce, he, Z, Re, Te, ot, Ie, Ee, jt = "LV.", dt, gt = s[0].level + "", it, ct, Ge, ft, pt = s[0].ascension * 20 + (s[0].ascension > 3 ? 10 : 20) + "", $t, Ht, Le, Xe, Rt, Ze, Lt, xe, Ft, Me, At, Et, S, qe, Ue, Kt, Bt, va = s[24](fa || (fa = nl([`
	<script>
		(() => {
			const card = document.querySelector('.card-scroll .Card');
			const host = document.querySelector('.card-scroll .card-host');
			const pepega = document.getElementById('pepega');
			const height = host.offsetHeight;
			const fuckyRatio = 100 / (pepega.offsetHeight || 100);
			const fontSize = (height / 30) * fuckyRatio;
			card.style.fontSize = fontSize + 'px';
			card.style.setProperty('--fontSize', fontSize + 'px');
		})();
	<\/script>
`]))) + "", Gt, et, el, Qt, ut, We, He = !s[18] && sa();
    L = new qa({
        props: {
            $$slots: {
                default: [Rs]
            },
            $$scope: {
                ctx: s
            }
        }
    }),
    ke = new ms({
        props: {
            avatar: s[0]
        }
    });
    let we = s[19] && ia(s);
    pe = new Mt({
        props: {
            name: s[0].meta.element
        }
    }),
    ie = new ga({
        props: {
            rarity: s[0].meta.rarity
        }
    }),
    Z = new pa({
        props: {
            level: s[0].const
        }
    }),
    Te = new ws({
        props: {
            level: s[0].ascension
        }
    }),
    Xe = new $s({
        props: {
            avatar: s[0]
        }
    }),
    Ze = new Hs({
        props: {
            avatar: s[0]
        }
    }),
    xe = new da({
        props: {
            avatar: s[0],
            ship: !0
        }
    });
    function sl(v, U) {
        return v[21] ? Fs : Ls
    }
    let Yt = sl(s)
      , ze = Yt(s)
      , ye = (s[7].nickname && (s[17] || s[4]) || !s[4] && !s[17]) && ra(s)
      , Ce = (!s[17] && !s[4] && s[22].uid || s[7].uid && (s[17] || s[4])) && na(s);
    function ba(v) {
        s[51](v)
    }
    let il = {
        build: s[3],
        local: s[4],
        $$slots: {
            default: [Bs]
        },
        $$scope: {
            ctx: s
        }
    };
    return s[2] !== void 0 && (il.edit = s[2]),
    et = new Ra({
        props: il
    }),
    s[50](et),
    nt.push( () => Zt(et, "edit", ba)),
    ut = new La({
        props: {
            target: [s[9]],
            $$slots: {
                default: [Us]
            },
            $$scope: {
                ctx: s
            }
        }
    }),
    {
        c() {
            e = b("link"),
            l = b("link"),
            t = b("script"),
            t.innerHTML = a,
            r = b("script"),
            r.innerHTML = o,
            f = H(),
            c = b("div"),
            c.textContent = u,
            m = H(),
            A = b("div"),
            P = b("div"),
            p = b("img"),
            w = H(),
            _ = b("div"),
            V = b("div"),
            T = H(),
            N = b("div"),
            G = H(),
            ae = b("div"),
            x = H(),
            He && He.c(),
            $ = H(),
            O = b("div"),
            B = H(),
            j(L.$$.fragment),
            ge = H(),
            fe = b("div"),
            j(ke.$$.fragment),
            C = H(),
            le = b("div"),
            ne = b("div"),
            we && we.c(),
            Ne = H(),
            Ve = b("div"),
            $e = b("div"),
            j(pe.$$.fragment),
            Be = H(),
            j(ie.$$.fragment),
            oe = H(),
            re = b("div"),
            ue = b("div"),
            X = b("img"),
            F = H(),
            W = b("div"),
            Ae = De(se),
            ce = H(),
            he = b("div"),
            j(Z.$$.fragment),
            Re = H(),
            j(Te.$$.fragment),
            ot = H(),
            Ie = b("div"),
            Ee = b("span"),
            Ee.textContent = jt,
            dt = H(),
            it = De(gt),
            ct = H(),
            Ge = b("i"),
            ft = De("/"),
            $t = De(pt),
            Ht = H(),
            Le = b("div"),
            j(Xe.$$.fragment),
            Rt = H(),
            j(Ze.$$.fragment),
            Lt = H(),
            j(xe.$$.fragment),
            Ft = H(),
            Me = b("div"),
            ze.c(),
            At = H(),
            ye && ye.c(),
            Et = H(),
            Ce && Ce.c(),
            Kt = H(),
            Bt = new Aa(!1),
            Gt = H(),
            j(et.$$.fragment),
            Qt = H(),
            j(ut.$$.fragment),
            this.h()
        },
        l(v) {
            const U = Ea("svelte-14gojvq", document.head);
            e = k(U, "LINK", {
                rel: !0,
                href: !0
            }),
            l = k(U, "LINK", {
                rel: !0,
                href: !0
            }),
            t = k(U, "SCRIPT", {
                src: !0,
                "data-svelte-h": !0
            }),
            Dt(t) !== "svelte-1fvc1rs" && (t.innerHTML = a),
            r = k(U, "SCRIPT", {
                src: !0,
                "data-svelte-h": !0
            }),
            Dt(r) !== "svelte-1kioc85" && (r.innerHTML = o),
            U.forEach(h),
            f = R(v),
            c = k(v, "DIV", {
                id: !0,
                style: !0,
                "data-svelte-h": !0
            }),
            Dt(c) !== "svelte-iwexca" && (c.textContent = u),
            m = R(v),
            A = k(v, "DIV", {
                class: !0
            });
            var Ut = E(A);
            P = k(Ut, "DIV", {
                class: !0,
                style: !0
            });
            var vt = E(P);
            p = k(vt, "IMG", {
                class: !0,
                src: !0,
                alt: !0
            }),
            w = R(vt),
            _ = k(vt, "DIV", {
                class: !0
            });
            var _e = E(_);
            V = k(_e, "DIV", {
                class: !0
            }),
            E(V).forEach(h),
            T = R(_e),
            N = k(_e, "DIV", {
                class: !0
            }),
            E(N).forEach(h),
            G = R(_e),
            ae = k(_e, "DIV", {
                class: !0
            }),
            E(ae).forEach(h),
            x = R(_e),
            He && He.l(_e),
            $ = R(_e),
            O = k(_e, "DIV", {
                class: !0
            }),
            E(O).forEach(h),
            B = R(_e),
            K(L.$$.fragment, _e),
            ge = R(_e),
            fe = k(_e, "DIV", {
                class: !0
            });
            var Wt = E(fe);
            K(ke.$$.fragment, Wt),
            Wt.forEach(h),
            C = R(_e),
            le = k(_e, "DIV", {
                class: !0
            });
            var bt = E(le);
            ne = k(bt, "DIV", {
                class: !0
            });
            var rt = E(ne);
            we && we.l(rt),
            Ne = R(rt),
            Ve = k(rt, "DIV", {
                class: !0
            });
            var kt = E(Ve);
            $e = k(kt, "DIV", {
                class: !0
            });
            var Ot = E($e);
            K(pe.$$.fragment, Ot),
            Ot.forEach(h),
            Be = R(kt),
            K(ie.$$.fragment, kt),
            kt.forEach(h),
            oe = R(rt),
            re = k(rt, "DIV", {
                class: !0
            });
            var It = E(re);
            ue = k(It, "DIV", {
                class: !0
            });
            var ht = E(ue);
            X = k(ht, "IMG", {
                src: !0,
                class: !0
            }),
            ht.forEach(h),
            F = R(It),
            W = k(It, "DIV", {
                class: !0
            });
            var wt = E(W);
            Ae = Se(wt, se),
            wt.forEach(h),
            It.forEach(h),
            rt.forEach(h),
            ce = R(bt),
            he = k(bt, "DIV", {
                class: !0
            });
            var yt = E(he);
            K(Z.$$.fragment, yt),
            Re = R(yt),
            K(Te.$$.fragment, yt),
            ot = R(yt),
            Ie = k(yt, "DIV", {
                class: !0
            });
            var Ct = E(Ie);
            Ee = k(Ct, "SPAN", {
                class: !0,
                "data-svelte-h": !0
            }),
            Dt(Ee) !== "svelte-1mbawbm" && (Ee.textContent = jt),
            dt = R(Ct),
            it = Se(Ct, gt),
            ct = R(Ct),
            Ge = k(Ct, "I", {
                class: !0
            });
            var tl = E(Ge);
            ft = Se(tl, "/"),
            $t = Se(tl, pt),
            tl.forEach(h),
            Ct.forEach(h),
            yt.forEach(h),
            bt.forEach(h),
            Ht = R(_e),
            Le = k(_e, "DIV", {
                class: !0
            });
            var _t = E(Le);
            K(Xe.$$.fragment, _t),
            Rt = R(_t),
            K(Ze.$$.fragment, _t),
            Lt = R(_t),
            K(xe.$$.fragment, _t),
            Ft = R(_t),
            Me = k(_t, "DIV", {
                class: !0
            });
            var Pt = E(Me);
            ze.l(Pt),
            At = R(Pt),
            ye && ye.l(Pt),
            Et = R(Pt),
            Ce && Ce.l(Pt),
            Pt.forEach(h),
            _t.forEach(h),
            _e.forEach(h),
            vt.forEach(h),
            Ut.forEach(h),
            Kt = R(v),
            Bt = wa(v, !1),
            Gt = R(v),
            K(et.$$.fragment, v),
            Qt = R(v),
            K(ut.$$.fragment, v),
            this.h()
        },
        h() {
            d(e, "rel", "stylesheet"),
            d(e, "href", " /js/tooltip/v2/styles/fonts.css"),
            d(l, "rel", "stylesheet"),
            d(l, "href", " /js/tooltip/v2/styles/style.css"),
            Ke(t.src, i = " /js/tooltip/v2/modules/zzz.js?i") || d(t, "src", i),
            t.defer = !0,
            Ke(r.src, n = " /js/tooltip/v2/script.js?i") || d(r, "src", n),
            r.defer = !0,
            d(c, "id", "pepega"),
            te(c, "font-size", "100px"),
            te(c, "line-height", "1"),
            te(c, "position", "absolute"),
            te(c, "visibility", "hidden"),
            te(c, "pointer-events", "none"),
            d(p, "class", "spacer svelte-pxa2i2"),
            Ke(p.src, D = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAFCAQAAADbc8WkAAAAD0lEQVR42mNkwAEY6SABAAH0AAY7BlaIAAAAAElFTkSuQmCC") || d(p, "src", D),
            d(p, "alt", ""),
            d(V, "class", "bg svelte-pxa2i2"),
            d(N, "class", "bg contour svelte-pxa2i2"),
            d(ae, "class", "bg fade svelte-pxa2i2"),
            d(O, "class", "bg dither svelte-pxa2i2"),
            d(fe, "class", "left svelte-pxa2i2"),
            d($e, "class", "el svelte-pxa2i2"),
            d(Ve, "class", "elstar svelte-pxa2i2"),
            Ke(X.src, st = "/ui/ef/profession/" + s[0].meta.role + ".png") || d(X, "src", st),
            d(X, "class", "svelte-pxa2i2"),
            d(ue, "class", "prof svelte-pxa2i2"),
            d(W, "class", "name svelte-pxa2i2"),
            d(re, "class", "profname svelte-pxa2i2"),
            d(ne, "class", "info svelte-pxa2i2"),
            d(Ee, "class", "svelte-pxa2i2"),
            d(Ge, "class", "svelte-pxa2i2"),
            d(Ie, "class", "level efnum svelte-pxa2i2"),
            d(he, "class", "levels svelte-pxa2i2"),
            d(le, "class", "middle svelte-pxa2i2"),
            d(Me, "class", "meta svelte-pxa2i2"),
            d(Le, "class", "right svelte-pxa2i2"),
            d(_, "class", S = "card-host " + s[0].meta.element + " svelte-pxa2i2"),
            ya( () => s[46].call(_)),
            d(P, "class", "Card svelte-pxa2i2"),
            d(P, "style", Ue = "font-size: " + s[8] + "px !important; --fontSize: " + s[8] + "px; --timing: 0.2s; --elementColor: " + s[12] + "; " + (s[18] || "") + ";"),
            z(P, "inScreenshot", s[11]),
            d(A, "class", "card-scroll svelte-pxa2i2"),
            z(A, "noInteract", Os),
            z(A, "compressed", s[5] && !s[11] && !s[2]),
            Bt.a = Gt
        },
        m(v, U) {
            g(document.head, e),
            g(document.head, l),
            g(document.head, t),
            g(document.head, r),
            M(v, f, U),
            M(v, c, U),
            s[44](c),
            M(v, m, U),
            M(v, A, U),
            g(A, P),
            g(P, p),
            g(P, w),
            g(P, _),
            g(_, V),
            g(_, T),
            g(_, N),
            g(_, G),
            g(_, ae),
            g(_, x),
            He && He.m(_, null),
            g(_, $),
            g(_, O),
            g(_, B),
            Q(L, _, null),
            g(_, ge),
            g(_, fe),
            Q(ke, fe, null),
            g(_, C),
            g(_, le),
            g(le, ne),
            we && we.m(ne, null),
            g(ne, Ne),
            g(ne, Ve),
            g(Ve, $e),
            Q(pe, $e, null),
            g(Ve, Be),
            Q(ie, Ve, null),
            g(ne, oe),
            g(ne, re),
            g(re, ue),
            g(ue, X),
            g(re, F),
            g(re, W),
            g(W, Ae),
            g(le, ce),
            g(le, he),
            Q(Z, he, null),
            g(he, Re),
            Q(Te, he, null),
            g(he, ot),
            g(he, Ie),
            g(Ie, Ee),
            g(Ie, dt),
            g(Ie, it),
            g(Ie, ct),
            g(Ie, Ge),
            g(Ge, ft),
            g(Ge, $t),
            g(_, Ht),
            g(_, Le),
            Q(Xe, Le, null),
            g(Le, Rt),
            Q(Ze, Le, null),
            g(Le, Lt),
            Q(xe, Le, null),
            g(Le, Ft),
            g(Le, Me),
            ze.m(Me, null),
            g(Me, At),
            ye && ye.m(Me, null),
            g(Me, Et),
            Ce && Ce.m(Me, null),
            qe = Ca(_, s[46].bind(_)),
            s[47](_),
            s[48](P),
            M(v, Kt, U),
            Bt.m(va, v, U),
            M(v, Gt, U),
            Q(et, v, U),
            M(v, Qt, U),
            Q(ut, v, U),
            We = !0
        },
        p(v, U) {
            v[18] ? He && (He.d(1),
            He = null) : He || (He = sa(),
            He.c(),
            He.m(_, $));
            const Ut = {};
            U[0] & 1029 | U[2] & 64 && (Ut.$$scope = {
                dirty: U,
                ctx: v
            }),
            L.$set(Ut);
            const vt = {};
            U[0] & 1 && (vt.avatar = v[0]),
            ke.$set(vt),
            v[19] ? we ? we.p(v, U) : (we = ia(v),
            we.c(),
            we.m(ne, Ne)) : we && (we.d(1),
            we = null);
            const _e = {};
            U[0] & 1 && (_e.name = v[0].meta.element),
            pe.$set(_e);
            const Wt = {};
            U[0] & 1 && (Wt.rarity = v[0].meta.rarity),
            ie.$set(Wt),
            (!We || U[0] & 1 && !Ke(X.src, st = "/ui/ef/profession/" + v[0].meta.role + ".png")) && d(X, "src", st),
            (!We || U[0] & 1048577) && se !== (se = v[20](v[0].meta.nameHash) + "") && Fe(Ae, se);
            const bt = {};
            U[0] & 1 && (bt.level = v[0].const),
            Z.$set(bt);
            const rt = {};
            U[0] & 1 && (rt.level = v[0].ascension),
            Te.$set(rt),
            (!We || U[0] & 1) && gt !== (gt = v[0].level + "") && Fe(it, gt),
            (!We || U[0] & 1) && pt !== (pt = v[0].ascension * 20 + (v[0].ascension > 3 ? 10 : 20) + "") && Fe($t, pt);
            const kt = {};
            U[0] & 1 && (kt.avatar = v[0]),
            Xe.$set(kt);
            const Ot = {};
            U[0] & 1 && (Ot.avatar = v[0]),
            Ze.$set(Ot);
            const It = {};
            U[0] & 1 && (It.avatar = v[0]),
            xe.$set(It),
            Yt === (Yt = sl(v)) && ze ? ze.p(v, U) : (ze.d(1),
            ze = Yt(v),
            ze && (ze.c(),
            ze.m(Me, At))),
            v[7].nickname && (v[17] || v[4]) || !v[4] && !v[17] ? ye ? ye.p(v, U) : (ye = ra(v),
            ye.c(),
            ye.m(Me, Et)) : ye && (ye.d(1),
            ye = null),
            !v[17] && !v[4] && v[22].uid || v[7].uid && (v[17] || v[4]) ? Ce ? Ce.p(v, U) : (Ce = na(v),
            Ce.c(),
            Ce.m(Me, null)) : Ce && (Ce.d(1),
            Ce = null),
            (!We || U[0] & 1 && S !== (S = "card-host " + v[0].meta.element + " svelte-pxa2i2")) && d(_, "class", S),
            (!We || U[0] & 266496 && Ue !== (Ue = "font-size: " + v[8] + "px !important; --fontSize: " + v[8] + "px; --timing: 0.2s; --elementColor: " + v[12] + "; " + (v[18] || "") + ";")) && d(P, "style", Ue),
            (!We || U[0] & 2048) && z(P, "inScreenshot", v[11]),
            (!We || U[0] & 2084) && z(A, "compressed", v[5] && !v[11] && !v[2]);
            const ht = {};
            U[0] & 8 && (ht.build = v[3]),
            U[0] & 16 && (ht.local = v[4]),
            U[0] & 2048 | U[2] & 64 && (ht.$$scope = {
                dirty: U,
                ctx: v
            }),
            !el && U[0] & 4 && (el = !0,
            ht.edit = v[2],
            Xt( () => el = !1)),
            et.$set(ht);
            const wt = {};
            U[0] & 512 && (wt.target = [v[9]]),
            U[0] & 8519824 | U[2] & 64 && (wt.$$scope = {
                dirty: U,
                ctx: v
            }),
            ut.$set(wt)
        },
        i(v) {
            We || (I(L.$$.fragment, v),
            I(ke.$$.fragment, v),
            I(pe.$$.fragment, v),
            I(ie.$$.fragment, v),
            I(Z.$$.fragment, v),
            I(Te.$$.fragment, v),
            I(Xe.$$.fragment, v),
            I(Ze.$$.fragment, v),
            I(xe.$$.fragment, v),
            I(et.$$.fragment, v),
            I(ut.$$.fragment, v),
            We = !0)
        },
        o(v) {
            y(L.$$.fragment, v),
            y(ke.$$.fragment, v),
            y(pe.$$.fragment, v),
            y(ie.$$.fragment, v),
            y(Z.$$.fragment, v),
            y(Te.$$.fragment, v),
            y(Xe.$$.fragment, v),
            y(Ze.$$.fragment, v),
            y(xe.$$.fragment, v),
            y(et.$$.fragment, v),
            y(ut.$$.fragment, v),
            We = !1
        },
        d(v) {
            v && (h(f),
            h(c),
            h(m),
            h(A),
            h(Kt),
            Bt.d(),
            h(Gt),
            h(Qt)),
            h(e),
            h(l),
            h(t),
            h(r),
            s[44](null),
            He && He.d(),
            Y(L),
            Y(ke),
            we && we.d(),
            Y(pe),
            Y(ie),
            Y(Z),
            Y(Te),
            Y(Xe),
            Y(Ze),
            Y(xe),
            ze.d(),
            ye && ye.d(),
            Ce && Ce.d(),
            qe(),
            s[47](null),
            s[48](null),
            s[50](null),
            Y(et, v),
            Y(ut, v)
        }
    }
}
let Os = !1;
const qs = () => {}
  , zs = s => s.stopPropagation()
  , js = s => s.stopPropagation();
function Ks(s, e, l) {
    let t, a, i, r, o, n, f, c, u, m, A, P = be, p = () => (P(),
    P = Jt(o, S => l(59, A = S)),
    o), D, w = be, _ = () => (w(),
    w = Jt(a, S => l(41, D = S)),
    a), V, T, N, G, ae, x, $, O, B = be, L = () => (B(),
    B = Jt(r, S => l(19, O = S)),
    r), ge, fe, ke = be, C = () => (ke(),
    ke = Jt(i, S => l(21, fe = S)),
    i), le, ne;
    ve(s, Ha, S => l(60, T = S)),
    ve(s, Na, S => l(43, x = S)),
    s.$$.on_destroy.push( () => P()),
    s.$$.on_destroy.push( () => w()),
    s.$$.on_destroy.push( () => B()),
    s.$$.on_destroy.push( () => ke());
    const Ne = String.raw
      , {t: Ve, ef: $e, locale: pe} = at("l10n");
    ve(s, Ve, S => l(23, ne = S)),
    ve(s, $e, S => l(20, ge = S));
    const Be = at("globalToggles");
    ve(s, Be, S => l(7, V = S));
    let {build: ie=null} = e
      , {avatar: oe=ie == null ? void 0 : ie.avatar} = e
      , {local: re=!1} = e
      , {height: ue=void 0} = e
      , {compressed: X=!1} = e;
    const st = at("CardSettings");
    ve(s, st, S => l(42, ae = S));
    const F = at("PlayerInfo");
    ve(s, F, S => l(22, le = S));
    const W = qt("HighlightedProps", Nt());
    ve(s, W, S => l(62, G = S));
    let se = 18.066, Ae, ce = {
        canvas: null,
        cardHost: null,
        draggable: null,
        pepega: null,
        cardToggles: null
    }, he = !1;
    function Z(S=window.GestureEvent ? 1 : 1.5) {
        l(11, he = !0),
        lt(ft, N = [], N),
        domtoimage.toBlob(Ae, {
            width: Ae.offsetWidth,
            height: Ae.offsetHeight,
            scale: S,
            filter: qe => qe.tagName !== "IFRAME"
        }).then(function(qe) {
            var Ue = new Image;
            Ue.onload = () => {
                T.display(Ba, {
                    img: Ue
                }),
                console.log("SELENIUM:" + Ue.src),
                l(11, he = !1)
            }
            ,
            Ue.src = URL.createObjectURL(qe)
        })
    }
    const Re = Nt(null);
    ve(s, Re, S => l(18, $ = S));
    function Te(S) {
        if (!n || !S || !S.length) {
            Re.set(null);
            return
        }
        const qe = `--adaptiveGradient: linear-gradient(180deg, ${S[0]} 0%, ${S[1]} 50%,  ${S[2]} 100%);
--fadeGradient: linear-gradient(180deg, ${S[0]} 0%, ${S[1]}00 50%,  ${S[2]}) 100%`;
        Re.set(qe)
    }
    function ot(S) {
        m.getLayer("color").draw()
    }
    let Ie = 1
      , Ee = !1;
    ha( () => {
        var S;
        l(37, Ie = 100 / (((S = ce.pepega) == null ? void 0 : S.offsetHeight) || 100)),
        l(1, ue = ce.cardHost.offsetHeight),
        l(8, se = ue / 30 * Ie),
        l(38, Ee = !0)
    }
    ),
    Oa(S => {}
    );
    const jt = [{
        id: "splash",
        type: Vt.DEFAULT,
        anchor: {
            x: .5,
            y: .5
        },
        position: {
            x: .48,
            y: .46
        },
        height: 1,
        scale: 1.6,
        limits: new cl(.8,.2,.2,.8)
    }, {
        id: "local",
        type: Vt.CUSTOM_FIXED,
        anchor: {
            x: 0,
            y: .5
        },
        position: {
            x: 0,
            y: .5
        },
        height: 1,
        locked: !0
    }, {
        id: "server",
        type: Vt.CUSTOM_FIXED,
        anchor: {
            x: 0,
            y: .5
        },
        position: {
            x: 0,
            y: .5
        },
        height: 1,
        locked: !0
    }, {
        id: "custom",
        type: Vt.CUSTOM,
        anchor: {
            x: .5,
            y: .5
        },
        position: {
            x: .49,
            y: .5
        },
        height: 1,
        scale: 1,
        limits: new cl(1,.2,.2,1),
        hidden: !0
    }, {
        id: "feather",
        type: Vt.EFFECT,
        effect: new za({
            direction: 3,
            stops: [[.2, "rgba(255,255,255,0.2)"], [.3, "rgba(255,255,255,0.3)"], [.4, "rgba(255,255,255,1)"], [.6, "rgba(255,255,255,1)"], [.7, "rgba(255,255,255,0.3)"], [.8, "rgba(255,255,255,0.2)"]]
        })
    }, {
        id: "color",
        type: Vt.EFFECT,
        effect: new ja({
            callback: Te
        })
    }]
      , dt = qt("CLC", Nt());
    ve(s, dt, S => l(40, m = S));
    async function gt() {
        m.splash.applyTransform(A || oe.splashImageOffset),
        await m.setImages(null, re ? null : await (ie == null ? void 0 : ie.getLocalImage()), ie == null ? void 0 : ie.image, oe.splashImage),
        dt.set(m)
    }
    let {edit: it=!1} = e;
    const ct = Nt();
    ve(s, ct, S => l(58, u = S));
    const Ge = Nt();
    ve(s, Ge, S => l(57, c = S)),
    qt("mainProp", ct),
    qt("subProp", Ge);
    const ft = Nt([]);
    ve(s, ft, S => l(61, N = S)),
    qt("highlight", ft);
    function pt(S) {
        nt[S ? "unshift" : "push"]( () => {
            ce.pepega = S,
            l(10, ce)
        }
        )
    }
    function $t(S) {
        nt[S ? "unshift" : "push"]( () => {
            ce.draggable = S,
            l(10, ce)
        }
        )
    }
    function Ht() {
        ue = this.offsetHeight,
        l(1, ue)
    }
    function Le(S) {
        nt[S ? "unshift" : "push"]( () => {
            ce.cardHost = S,
            l(10, ce)
        }
        )
    }
    function Xe(S) {
        nt[S ? "unshift" : "push"]( () => {
            Ae = S,
            l(9, Ae)
        }
        )
    }
    const Rt = () => Z();
    function Ze(S) {
        nt[S ? "unshift" : "push"]( () => {
            ce.cardToggles = S,
            l(10, ce)
        }
        )
    }
    function Lt(S) {
        it = S,
        l(2, it)
    }
    const xe = () => Z()
      , Ft = () => Z(3);
    function Me(S) {
        s.$$.not_equal(V.adaptiveColor, S) && (V.adaptiveColor = S,
        Be.set(V))
    }
    function At(S) {
        s.$$.not_equal(V.uid, S) && (V.uid = S,
        Be.set(V))
    }
    function Et(S) {
        s.$$.not_equal(V.nickname, S) && (V.nickname = S,
        Be.set(V))
    }
    return s.$$set = S => {
        "build"in S && l(3, ie = S.build),
        "avatar"in S && l(0, oe = S.avatar),
        "local"in S && l(4, re = S.local),
        "height"in S && l(1, ue = S.height),
        "compressed"in S && l(5, X = S.compressed),
        "edit"in S && l(2, it = S.edit)
    }
    ,
    s.$$.update = () => {
        var S, qe;
        if (s.$$.dirty[1] & 4096 && l(17, t = (qe = (S = x.data) == null ? void 0 : S.userInfo) == null ? void 0 : qe.me),
        s.$$.dirty[0] & 8 && ie && l(0, oe = ie.avatar),
        s.$$.dirty[1] & 2048 && _(l(16, {adaptiveColor: a, artSource: i, caption: r, transform: o} = ae, a, C(l(15, i)), L(l(14, r)), p(l(13, o)))),
        s.$$.dirty[0] & 1 && console.log(oe.meta.id),
        s.$$.dirty[0] & 144 | s.$$.dirty[1] & 1024 && l(39, n = re ? V.adaptiveColor : D),
        s.$$.dirty[0] & 1 | s.$$.dirty[1] & 896 && oe && Ee && m.loading === !1 && ot(),
        s.$$.dirty[0] & 2 | s.$$.dirty[1] & 64) {
            const Ue = ue / 30 * Ie;
            isNaN(Ue) || l(8, se = Ue)
        }
        s.$$.dirty[0] & 1 | s.$$.dirty[1] & 128 && Ee && oe && gt(),
        s.$$.dirty[0] & 1 && l(12, f = xt[oe.meta.element]),
        s.$$.dirty[0] & 1 && lt(ct, u = new q(oe.meta.excel.MainAttrId,0).simpleName, u),
        s.$$.dirty[0] & 1 && lt(Ge, c = new q(oe.meta.excel.SubAttrId,0).simpleName, c)
    }
    ,
    lt(W, G = [], G),
    [oe, ue, it, ie, re, X, Z, V, se, Ae, ce, he, f, o, r, i, a, t, $, O, ge, fe, le, ne, Ne, Ve, $e, Be, st, F, W, Re, jt, dt, ct, Ge, ft, Ie, Ee, n, m, D, ae, x, pt, $t, Ht, Le, Xe, Rt, Ze, Lt, xe, Ft, Me, At, Et]
}
class vi extends Ye {
    constructor(e) {
        super(),
        Je(this, e, Ks, Ws, Qe, {
            build: 3,
            avatar: 0,
            local: 4,
            height: 1,
            compressed: 5,
            toPng: 6,
            edit: 2
        }, null, [-1, -1, -1])
    }
    get toPng() {
        return this.$$.ctx[6]
    }
}
export {vi as E};
