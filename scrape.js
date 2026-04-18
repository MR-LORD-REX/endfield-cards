const I1 = {
    Avatar: h0,
    AvatarMeta: a1,
    Weapon: n1,
    WeaponMeta: o1,
    Relic: p1,
    RelicMeta: c1,
    PlayerInfo: m0,
    Property: G,
    Statistic: W,
    Rarities: E0
}
  , q0 = {
    Fire: "#ff9955",
    Water: "#3e99ff",
    Wind: "#80ffe6",
    Electric: "#b380ff",
    Grass: "#a5c83b",
    Ice: "#55ddff",
    Rock: "#ffcc00"
}
  , v0 = {
    4: "#8a54cb",
    5: "#e8a54c"
}
  , u1 = {
    4: {
        StrId: "chr_0007_ikut",
        NameHash: "7503679737956618234",
        Rarity: 5,
        Element: "Pulse",
        Profession: "VANGUARD",
        WeaponType: "Sword",
        MainAttrId: 40,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0007_ikut_3: {
                40: 15
            },
            chr_0007_ikut_1: {
                40: 10
            },
            chr_0007_ikut_7: {
                40: 20
            },
            chr_0007_ikut_5: {
                40: 15
            }
        },
        SkillInfoMap: {
            56: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_ikut_01.png",
                Element: "Physical"
            },
            8: {
                Icon: "/ui/ef/skillicon/icon_skill_ikut_01.png",
                Element: "Pulse"
            },
            9: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_ikut_01.png",
                Element: "Pulse"
            },
            7: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0007_ikut_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_ikut_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0007_ikut_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0007_ikut_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0007_ikut_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0007_ikut_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_ikut_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0007_ikut_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0007_ikut_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_ikut_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0007_ikut_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_ikut_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                40: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                41: {
                    Value: 15,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 80, 83, 86, 89, 92, 95, 98, 101, 104, 107, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 142, 145, 148, 151, 154, 157, 160, 163, 166, 169, 173, 176, 179, 182, 185, 188, 191, 194, 197, 200, 204, 207, 210, 213, 216, 219, 222, 225, 228, 231, 235, 238, 241, 244, 247, 250, 253, 256, 259, 262, 266, 269, 272, 275, 278, 281, 284, 287, 290, 293, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 328, 331, 334],
        BaseAttributes: {
            39: {
                BaseValue: 14.02061855670108,
                AddValue: 1.0498632442667784
            },
            40: {
                BaseValue: 14.690721649484539,
                AddValue: 1.4690721649484582
            },
            41: {
                BaseValue: 12.4742268041237,
                AddValue: 1.2474226804123747
            },
            42: {
                BaseValue: 10.10309278350519,
                AddValue: 1.010309278350515
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 5,
                AddValue: 0
            },
            12: {
                BaseValue: 5,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    6: {
        StrId: "chr_0009_azrila",
        NameHash: "5028992047801557402",
        Rarity: 6,
        Element: "Fire",
        Profession: "DEFENDER",
        WeaponType: "Claymores",
        MainAttrId: 39,
        SubAttrId: 42,
        AttributeNodes: {
            chr_0009_azrila_1: {
                39: 10
            },
            chr_0009_azrila_3: {
                39: 15
            },
            chr_0009_azrila_5: {
                39: 15
            },
            chr_0009_azrila_7: {
                39: 20
            }
        },
        SkillInfoMap: {
            23: {
                Icon: "/ui/ef/skillicon/icon_skill_azrila_01.png",
                Element: "Fire"
            },
            24: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_azrila_01.png",
                Element: "Fire"
            },
            54: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_azrila_01.png",
                Element: "Physical"
            },
            22: {
                Icon: "/ui/ef/skillicon/icon_attack_claym.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0009_azrila_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_azrila_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0009_azrila_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_azrila_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0009_azrila_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0009_azrila_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0009_azrila_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0009_azrila_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0009_azrila_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_azrila_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0009_azrila_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_azrila_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                39: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                42: {
                    Value: 20,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 46, 50, 53, 56, 60, 63, 66, 70, 73, 76, 79, 83, 86, 89, 93, 96, 99, 103, 106, 109, 112, 116, 119, 122, 126, 129, 132, 136, 139, 142, 145, 149, 152, 155, 159, 162, 165, 168, 172, 175, 178, 182, 185, 188, 192, 195, 198, 201, 205, 208, 211, 215, 218, 221, 225, 228, 231, 234, 238, 241, 244, 248, 251, 254, 258, 261, 264, 267, 271, 274, 277, 281, 284, 287, 291, 294, 297, 300, 304, 307, 310, 314, 317, 320, 323, 327, 330, 333, 337, 340, 343, 347, 350, 353],
        BaseAttributes: {
            39: {
                BaseValue: 21.64948453608248,
                AddValue: 1.738901746265522
            },
            40: {
                BaseValue: 9.793814432989725,
                AddValue: .9793814432989686
            },
            41: {
                BaseValue: 8.762886597938175,
                AddValue: .876288659793814
            },
            42: {
                BaseValue: 13.6082474226804,
                AddValue: 1.19835893120135
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    8: {
        StrId: "chr_0011_seraph",
        NameHash: "1803181259851624411",
        Rarity: 5,
        Element: "Cryst",
        Profession: "SUPPORTER",
        WeaponType: "Wand",
        MainAttrId: 42,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0011_seraph_7: {
                42: 20
            },
            chr_0011_seraph_5: {
                42: 15
            },
            chr_0011_seraph_3: {
                42: 15
            },
            chr_0011_seraph_1: {
                42: 10
            }
        },
        SkillInfoMap: {
            12: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_seraph_01.png",
                Element: "Cryst"
            },
            53: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_seraph_01.png",
                Element: "Cryst"
            },
            10: {
                Icon: "/ui/ef/skillicon/icon_attack_funnel.png",
                Element: "Cryst"
            },
            11: {
                Icon: "/ui/ef/skillicon/icon_skill_seraph_01.png",
                Element: "Cryst"
            }
        },
        NodeSkillMap: {
            fac_chr_0011_seraph_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0011_seraph_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0011_seraph_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0011_seraph_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_seraph_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0011_seraph_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0011_seraph_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_seraph_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0011_seraph_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_seraph_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 4,
            Attrs: {
                41: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                29: {
                    Value: .1,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 89, 92, 95, 97, 100, 103, 106, 109, 112, 115, 118, 121, 124, 127, 130, 133, 136, 139, 141, 144, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 185, 188, 191, 194, 197, 200, 203, 206, 209, 212, 215, 218, 221, 224, 227, 230, 232, 235, 238, 241, 244, 247, 250, 253, 256, 259, 262, 265, 268, 271, 274, 276, 279, 282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318],
        BaseAttributes: {
            39: {
                BaseValue: 9.329896907216527,
                AddValue: .9045865768988004
            },
            40: {
                BaseValue: 9.381443298969105,
                AddValue: .9267830843677672
            },
            41: {
                BaseValue: 15.876288659793799,
                AddValue: 1.250199873763942
            },
            42: {
                BaseValue: 15.154639175257735,
                AddValue: 1.5154639175257782
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    10: {
        StrId: "chr_0004_pelica",
        NameHash: "7201533996830628902",
        Rarity: 5,
        Element: "Pulse",
        Profession: "CASTER",
        WeaponType: "Wand",
        MainAttrId: 41,
        SubAttrId: 42,
        AttributeNodes: {
            chr_0004_pelica_7: {
                41: 20
            },
            chr_0004_pelica_5: {
                41: 15
            },
            chr_0004_pelica_3: {
                41: 15
            },
            chr_0004_pelica_1: {
                41: 10
            }
        },
        SkillInfoMap: {
            36: {
                Icon: "/ui/ef/skillicon/icon_skill_pelica_01.png",
                Element: "Pulse"
            },
            37: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_pelica_01.png",
                Element: "Pulse"
            },
            35: {
                Icon: "/ui/ef/skillicon/icon_attack_funnel.png",
                Element: "Pulse"
            },
            38: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_pelica_01.png",
                Element: "Pulse"
            }
        },
        NodeSkillMap: {
            fac_chr_0004_pelica_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0004_pelica_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0004_pelica_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_pelica_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0004_pelica_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_pelica_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0004_pelica_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_pelica_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0004_pelica_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0004_pelica_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 2,
                Type: 5
            }
        },
        PotAttributes: [],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 97, 101, 104, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 137, 140, 143, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 186, 189, 193, 196, 199, 202, 205, 208, 211, 214, 217, 220, 223, 226, 229, 232, 235, 238, 242, 245, 248, 251, 254, 257, 260, 263, 266, 269, 272, 275, 278, 281, 284, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327, 330],
        BaseAttributes: {
            39: {
                BaseValue: 9.27835051546395,
                AddValue: .9278350515463912
            },
            40: {
                BaseValue: 9.48453608247426,
                AddValue: .9484536082474222
            },
            41: {
                BaseValue: 21.64948453608248,
                AddValue: 1.5735956238165423
            },
            42: {
                BaseValue: 13.6082474226804,
                AddValue: 1.1233747107090288
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    11: {
        StrId: "chr_0012_avywen",
        NameHash: "5709646229592187150",
        Rarity: 5,
        Element: "Pulse",
        Profession: "ASSAULT",
        WeaponType: "Lance",
        MainAttrId: 42,
        SubAttrId: 40,
        AttributeNodes: {
            chr_0012_avywen_5: {
                42: 15
            },
            chr_0012_avywen_7: {
                42: 20
            },
            chr_0012_avywen_1: {
                42: 10
            },
            chr_0012_avywen_3: {
                42: 15
            }
        },
        SkillInfoMap: {
            51: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_avywen_01.png",
                Element: "Pulse"
            },
            25: {
                Icon: "/ui/ef/skillicon/icon_attack_lance.png",
                Element: "Physical"
            },
            26: {
                Icon: "/ui/ef/skillicon/icon_skill_avywen_01.png",
                Element: "Pulse"
            },
            27: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_avywen_01.png",
                Element: "Pulse"
            }
        },
        NodeSkillMap: {
            chr_0012_avywen_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_avywen_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0012_avywen_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_avywen_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0012_avywen_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0012_avywen_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0012_avywen_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0012_avywen_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0012_avywen_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_avywen_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0012_avywen_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_avywen_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 3,
            Attrs: {
                42: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                52: {
                    Value: .08,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 43, 46, 49, 52, 55, 58, 62, 65, 68, 71, 74, 77, 81, 84, 87, 90, 93, 96, 100, 103, 106, 109, 112, 115, 119, 122, 125, 128, 131, 134, 138, 141, 144, 147, 150, 153, 157, 160, 163, 166, 169, 172, 176, 179, 182, 185, 188, 191, 195, 198, 201, 204, 207, 210, 214, 217, 220, 223, 226, 229, 233, 236, 239, 242, 245, 248, 252, 255, 258, 261, 264, 267, 271, 274, 277, 280, 283, 286, 290, 293, 296, 299, 302, 305, 309, 312, 315, 318, 321, 324, 328, 331, 334, 337, 340],
        BaseAttributes: {
            39: {
                BaseValue: 12.886597938144375,
                AddValue: 1.0614348832316427
            },
            40: {
                BaseValue: 10.77319587628865,
                AddValue: 1.0773195876288688
            },
            41: {
                BaseValue: 14.123711340206237,
                AddValue: 1.0828950136755728
            },
            42: {
                BaseValue: 15.000000000000004,
                AddValue: 1.5000000000000047
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    12: {
        StrId: "chr_0013_aglina",
        NameHash: "5075663083436839087",
        Rarity: 6,
        Element: "Natural",
        Profession: "SUPPORTER",
        WeaponType: "Wand",
        MainAttrId: 42,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0013_aglina_3: {
                42: 15
            },
            chr_0013_aglina_1: {
                42: 10
            },
            chr_0013_aglina_7: {
                42: 20
            },
            chr_0013_aglina_5: {
                42: 15
            }
        },
        SkillInfoMap: {
            14: {
                Icon: "/ui/ef/skillicon/icon_skill_aglina_01.png",
                Element: "Natural"
            },
            15: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_aglina_01.png",
                Element: "Natural"
            },
            16: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_aglina_01.png",
                Element: "Natural"
            },
            13: {
                Icon: "/ui/ef/skillicon/icon_attack_funnel.png",
                Element: "Natural"
            }
        },
        NodeSkillMap: {
            chr_0013_aglina_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_aglina_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0013_aglina_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_aglina_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0013_aglina_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0013_aglina_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0013_aglina_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0013_aglina_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0013_aglina_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_aglina_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0013_aglina_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_aglina_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 47, 50, 54, 57, 60, 64, 67, 70, 74, 77, 80, 84, 87, 91, 94, 97, 101, 104, 107, 111, 114, 117, 121, 124, 128, 131, 134, 138, 141, 144, 148, 151, 154, 158, 161, 165, 168, 171, 175, 178, 181, 185, 188, 191, 195, 198, 202, 205, 208, 212, 215, 218, 222, 225, 228, 232, 235, 239, 242, 245, 249, 252, 255, 259, 262, 265, 269, 272, 276, 279, 282, 286, 289, 292, 296, 299, 302, 306, 309, 313, 316, 319, 323, 326, 329, 333, 336, 339, 343, 346, 350, 353, 356, 360],
        BaseAttributes: {
            39: {
                BaseValue: 9.07216494845364,
                AddValue: .9072164948453605
            },
            40: {
                BaseValue: 9.381443298969105,
                AddValue: .9381443298969069
            },
            41: {
                BaseValue: 16.10309278350514,
                AddValue: 1.247885545970969
            },
            42: {
                BaseValue: 20.412371134020624,
                AddValue: 1.700399747527883
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    13: {
        StrId: "chr_0005_chen",
        NameHash: "3128157701878862541",
        Rarity: 5,
        Element: "Physical",
        Profession: "GUARD",
        WeaponType: "Sword",
        MainAttrId: 40,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0005_chen_5: {
                40: 15
            },
            chr_0005_chen_7: {
                40: 20
            },
            chr_0005_chen_1: {
                40: 10
            },
            chr_0005_chen_3: {
                40: 15
            }
        },
        SkillInfoMap: {
            21: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_chen_01.png",
                Element: "Physical"
            },
            1: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            },
            2: {
                Icon: "/ui/ef/skillicon/icon_skill_chen_01.png",
                Element: "Physical"
            },
            3: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_chen_01.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0005_chen_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_chen_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0005_chen_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_chen_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0005_chen_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_chen_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0005_chen_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_chen_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0005_chen_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_mineral.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0005_chen_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0005_chen_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0005_chen_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_mineral.png",
                Level: 1,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                40: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                50: {
                    Value: .08,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 186, 189, 192, 195, 198, 201, 204, 207, 210, 213, 216, 219, 222, 225, 228, 231, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324],
        BaseAttributes: {
            39: {
                BaseValue: 10.77319587628865,
                AddValue: 1.0773195876288688
            },
            40: {
                BaseValue: 20.567010309278356,
                AddValue: 1.6988217967599468
            },
            41: {
                BaseValue: 8.86597938144333,
                AddValue: .8638754470860505
            },
            42: {
                BaseValue: 9.69072164948457,
                AddValue: .9463496738901742
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    14: {
        StrId: "chr_0006_wolfgd",
        NameHash: "-3531987865314967190",
        Rarity: 5,
        Element: "Fire",
        Profession: "CASTER",
        WeaponType: "Pistol",
        MainAttrId: 39,
        SubAttrId: 40,
        AttributeNodes: {
            chr_0006_wolfgd_3: {
                39: 15
            },
            chr_0006_wolfgd_5: {
                39: 15
            },
            chr_0006_wolfgd_7: {
                39: 20
            },
            chr_0006_wolfgd_1: {
                39: 10
            }
        },
        SkillInfoMap: {
            52: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_wolfgd_01.png",
                Element: "Fire"
            },
            28: {
                Icon: "/ui/ef/skillicon/icon_attack_pistol.png",
                Element: "Fire"
            },
            29: {
                Icon: "/ui/ef/skillicon/icon_skill_wolfgd_01.png",
                Element: "Fire"
            },
            30: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_wolfgd_01.png",
                Element: "Fire"
            }
        },
        NodeSkillMap: {
            chr_0006_wolfgd_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_wolfgd_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0006_wolfgd_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_wolfgd_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0006_wolfgd_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_wolfgd_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0006_wolfgd_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_wolfgd_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0006_wolfgd_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0006_wolfgd_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_mineral.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0006_wolfgd_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0006_wolfgd_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_mineral.png",
                Level: 2,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 1,
            Attrs: {
                39: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                40: {
                    Value: 15,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 77, 80, 83, 86, 89, 92, 95, 98, 101, 104, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 137, 140, 143, 146, 149, 152, 155, 158, 161, 164, 166, 169, 172, 175, 178, 181, 184, 187, 190, 193, 196, 199, 202, 205, 208, 211, 214, 217, 220, 223, 226, 229, 232, 235, 238, 241, 244, 247, 250, 253, 255, 258, 261, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321],
        BaseAttributes: {
            39: {
                BaseValue: 18.55670103092784,
                AddValue: 1.6085630128340047
            },
            40: {
                BaseValue: 9.63917525773195,
                AddValue: .9639175257731986
            },
            41: {
                BaseValue: 9.381443298969105,
                AddValue: .9381443298969069
            },
            42: {
                BaseValue: 13.81443298969077,
                AddValue: 1.0974121607405842
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    20: {
        StrId: "chr_0018_dapan",
        NameHash: "4641966554191326705",
        Rarity: 5,
        Element: "Physical",
        Profession: "ASSAULT",
        WeaponType: "Claymores",
        MainAttrId: 39,
        SubAttrId: 42,
        AttributeNodes: {
            chr_0018_dapan_5: {
                39: 15
            },
            chr_0018_dapan_7: {
                39: 20
            },
            chr_0018_dapan_3: {
                39: 15
            },
            chr_0018_dapan_1: {
                39: 10
            }
        },
        SkillInfoMap: {
            55: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_dapan_01.png",
                Element: "Physical"
            },
            17: {
                Icon: "/ui/ef/skillicon/icon_attack_claym.png",
                Element: "Physical"
            },
            18: {
                Icon: "/ui/ef/skillicon/icon_skill_dapan_01.png",
                Element: "Physical"
            },
            19: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_dapan_01.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0018_dapan_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_dapan_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0018_dapan_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0018_dapan_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0018_dapan_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_fungus.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            chr_0018_dapan_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_dapan_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0018_dapan_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_dapan_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0018_dapan_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_dapan_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0018_dapan_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_fungus.png",
                Level: 2,
                Index: 2,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 3,
            Attrs: {
                39: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                50: {
                    Value: .08,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 97, 101, 104, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 137, 140, 143, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 186, 189, 193, 196, 199, 202, 205, 208, 211, 214, 217, 220, 223, 226, 229, 232, 235, 238, 242, 245, 248, 251, 254, 257, 260, 263, 266, 269, 272, 275, 278, 281, 284, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327, 330],
        BaseAttributes: {
            39: {
                BaseValue: 24.278350515463924,
                AddValue: 1.6950347149168998
            },
            40: {
                BaseValue: 9.793814432989725,
                AddValue: .9793814432989686
            },
            41: {
                BaseValue: 10.10309278350519,
                AddValue: .9535030507048176
            },
            42: {
                BaseValue: 10.43298969072164,
                AddValue: 1.0308015989901143
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    22: {
        StrId: "chr_0002_endminm",
        NameHash: "-7078064683023630592",
        Rarity: 6,
        Element: "Physical",
        Profession: "GUARD",
        WeaponType: "Sword",
        MainAttrId: 40,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0002_endminm_7: {
                40: 20
            },
            chr_0002_endminm_1: {
                40: 10
            },
            chr_0002_endminm_5: {
                40: 15
            },
            chr_0002_endminm_3: {
                40: 15
            }
        },
        SkillInfoMap: {
            34: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_endmin_01.png",
                Element: "Physical"
            },
            31: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            },
            32: {
                Icon: "/ui/ef/skillicon/icon_skill_endmin_01.png",
                Element: "Physical"
            },
            33: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_endmin_01.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0002_endminm_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_endminm_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0002_endminm_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_endminm_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0002_endminm_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_endminm_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0002_endminm_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_endminm_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 4,
            Attrs: {
                1: {
                    Value: .1,
                    Formula: "BaseMultiplier"
                },
                60: {
                    Value: -.1,
                    Formula: "BaseAddition"
                },
                40: {
                    Value: 25,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 40, 43, 46, 49, 53, 56, 59, 62, 66, 69, 72, 75, 79, 82, 85, 88, 92, 95, 98, 101, 105, 108, 111, 114, 118, 121, 124, 127, 131, 134, 137, 140, 144, 147, 150, 153, 157, 160, 163, 166, 170, 173, 176, 179, 183, 186, 189, 192, 196, 199, 202, 205, 209, 212, 215, 218, 222, 225, 228, 231, 235, 238, 241, 244, 248, 251, 254, 257, 261, 264, 267, 270, 274, 277, 280, 283, 287, 290, 293, 296, 300, 303, 306, 309, 313, 316, 319, 322, 326, 329, 332, 335, 339, 342, 345, 348],
        BaseAttributes: {
            39: {
                BaseValue: 14.7422680412371,
                AddValue: 1.224279402482646
            },
            40: {
                BaseValue: 14.226804123711345,
                AddValue: 1.4226804123711387
            },
            41: {
                BaseValue: 9.793814432989725,
                AddValue: .9793814432989686
            },
            42: {
                BaseValue: 10.824742268041275,
                AddValue: 1.0824742268041232
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    23: {
        StrId: "chr_0016_laevat",
        NameHash: "-7854629517048772793",
        Rarity: 6,
        Element: "Fire",
        Profession: "ASSAULT",
        WeaponType: "Sword",
        MainAttrId: 41,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0016_laevat_7: {
                41: 20
            },
            chr_0016_laevat_5: {
                41: 15
            },
            chr_0016_laevat_3: {
                41: 15
            },
            chr_0016_laevat_1: {
                41: 10
            }
        },
        SkillInfoMap: {
            40: {
                Icon: "/ui/ef/skillicon/icon_skill_laevat_01.png",
                Element: "Fire"
            },
            41: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_laevat_01.png",
                Element: "Fire"
            },
            49: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_laevat_01.png",
                Element: "Fire"
            },
            39: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Fire"
            }
        },
        NodeSkillMap: {
            chr_0016_laevat_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_laevat_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0016_laevat_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0016_laevat_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0016_laevat_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_laevat_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0016_laevat_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_laevat_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0016_laevat_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_laevat_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0016_laevat_passive_skill_0_3: {
                Icon: "/ui/ef/icon_talent_laevat_01.png",
                Level: 3,
                Index: 0,
                Type: 4
            },
            fac_chr_0016_laevat_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0016_laevat_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 2,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                41: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                17: {
                    Value: .15,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 40, 43, 46, 49, 53, 56, 59, 62, 66, 69, 72, 75, 78, 82, 85, 88, 91, 95, 98, 101, 104, 108, 111, 114, 117, 120, 124, 127, 130, 133, 137, 140, 143, 146, 150, 153, 156, 159, 162, 166, 169, 172, 175, 179, 182, 185, 188, 192, 195, 198, 201, 204, 208, 211, 214, 217, 221, 224, 227, 230, 234, 237, 240, 243, 247, 250, 253, 256, 259, 263, 266, 269, 272, 276, 279, 282, 285, 289, 292, 295, 298, 301, 305, 308, 311, 314, 318, 321, 324, 327, 331, 334, 337, 340, 343, 347],
        BaseAttributes: {
            39: {
                BaseValue: 13.6082474226804,
                AddValue: 1.2108563012834035
            },
            40: {
                BaseValue: 9.587628865979415,
                AddValue: 1.0155691142436352
            },
            41: {
                BaseValue: 22.268041237113408,
                AddValue: 1.7496318114874874
            },
            42: {
                BaseValue: 9.07216494845364,
                AddValue: .9072164948453605
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 5,
                AddValue: 0
            },
            12: {
                BaseValue: 5,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    24: {
        StrId: "chr_0014_aurora",
        NameHash: "-6313235431437717749",
        Rarity: 5,
        Element: "Cryst",
        Profession: "DEFENDER",
        WeaponType: "Claymores",
        MainAttrId: 39,
        SubAttrId: 42,
        AttributeNodes: {
            chr_0014_aurora_1: {
                39: 10
            },
            chr_0014_aurora_3: {
                39: 15
            },
            chr_0014_aurora_5: {
                39: 15
            },
            chr_0014_aurora_7: {
                39: 20
            }
        },
        SkillInfoMap: {
            43: {
                Icon: "/ui/ef/skillicon/icon_skill_aurora_01.png",
                Element: "Cryst"
            },
            50: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_aurora_01.png",
                Element: "Cryst"
            },
            42: {
                Icon: "/ui/ef/skillicon/icon_attack_claym.png",
                Element: "Physical"
            },
            44: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_aurora_01.png",
                Element: "Cryst"
            }
        },
        NodeSkillMap: {
            chr_0014_aurora_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_aurora_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0014_aurora_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_aurora_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0014_aurora_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_aurora_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0014_aurora_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0014_aurora_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0014_aurora_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0014_aurora_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0014_aurora_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_aurora_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 4,
            Attrs: {
                3: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                42: {
                    Value: 20,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 186, 189, 192, 195, 198, 201, 204, 207, 210, 213, 216, 219, 222, 225, 228, 231, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324],
        BaseAttributes: {
            39: {
                BaseValue: 18.55670103092784,
                AddValue: 1.5318746055123131
            },
            40: {
                BaseValue: 12.3711340206186,
                AddValue: 1.036019356196086
            },
            41: {
                BaseValue: 9.48453608247426,
                AddValue: .9484536082474222
            },
            42: {
                BaseValue: 10.99999999999999,
                AddValue: 1.100000000000003
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    26: {
        StrId: "chr_0015_lifeng",
        NameHash: "-6840171208004431812",
        Rarity: 6,
        Element: "Physical",
        Profession: "GUARD",
        WeaponType: "Lance",
        MainAttrId: 40,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0015_lifeng_1: {
                40: 10
            },
            chr_0015_lifeng_7: {
                40: 20
            },
            chr_0015_lifeng_5: {
                40: 15
            },
            chr_0015_lifeng_3: {
                40: 15
            }
        },
        SkillInfoMap: {
            58: {
                Icon: "/ui/ef/skillicon/icon_skill_lifeng_01.png",
                Element: "Physical"
            },
            60: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_lifeng_01.png",
                Element: "Physical"
            },
            57: {
                Icon: "/ui/ef/skillicon/icon_attack_lance.png",
                Element: "Physical"
            },
            59: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_lifeng_01.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0015_lifeng_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_lifeng_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0015_lifeng_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0015_lifeng_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0015_lifeng_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0015_lifeng_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0015_lifeng_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_lifeng_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0015_lifeng_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_lifeng_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0015_lifeng_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_lifeng_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                39: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                40: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                41: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                42: {
                    Value: 15,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 43, 46, 49, 52, 55, 58, 62, 65, 68, 71, 74, 77, 81, 84, 87, 90, 93, 96, 100, 103, 106, 109, 112, 115, 119, 122, 125, 128, 131, 134, 138, 141, 144, 147, 150, 153, 157, 160, 163, 166, 169, 172, 176, 179, 182, 185, 188, 191, 195, 198, 201, 204, 207, 210, 214, 217, 220, 223, 226, 229, 233, 236, 239, 242, 245, 248, 252, 255, 258, 261, 264, 267, 271, 274, 277, 280, 283, 286, 290, 293, 296, 299, 302, 305, 309, 312, 315, 318, 321, 324, 328, 331, 334, 337, 340],
        BaseAttributes: {
            39: {
                BaseValue: 14.7422680412371,
                AddValue: 1.224279402482646
            },
            40: {
                BaseValue: 20.10309278350516,
                AddValue: 1.260467073427313
            },
            41: {
                BaseValue: 13.402061855670151,
                AddValue: 1.1470650115716383
            },
            42: {
                BaseValue: 12.886597938144375,
                AddValue: 1.1750473385230376
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    27: {
        StrId: "chr_0017_yvonne",
        NameHash: "-8634541419450148796",
        Rarity: 6,
        Element: "Cryst",
        Profession: "ASSAULT",
        WeaponType: "Pistol",
        MainAttrId: 41,
        SubAttrId: 40,
        AttributeNodes: {
            chr_0017_yvonne_1: {
                41: 10
            },
            chr_0017_yvonne_3: {
                41: 15
            },
            chr_0017_yvonne_5: {
                41: 15
            },
            chr_0017_yvonne_7: {
                41: 20
            }
        },
        SkillInfoMap: {
            62: {
                Icon: "/ui/ef/skillicon/icon_skill_yvonne_01.png",
                Element: "Cryst"
            },
            64: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_yvonne_01.png",
                Element: "Cryst"
            },
            61: {
                Icon: "/ui/ef/skillicon/icon_attack_pistol.png",
                Element: "Cryst"
            },
            63: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_yvonne_01.png",
                Element: "Cryst"
            }
        },
        NodeSkillMap: {
            chr_0017_yvonne_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_yvonne_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0017_yvonne_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_yvonne_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0017_yvonne_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_yvonne_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0017_yvonne_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_yvonne_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0017_yvonne_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_fungus.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0017_yvonne_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_fungus.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0017_yvonne_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0017_yvonne_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 1,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                41: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                9: {
                    Value: .07,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 46, 50, 53, 56, 59, 63, 66, 69, 72, 76, 79, 82, 85, 89, 92, 95, 99, 102, 105, 108, 112, 115, 118, 121, 125, 128, 131, 134, 138, 141, 144, 148, 151, 154, 157, 161, 164, 167, 170, 174, 177, 180, 183, 187, 190, 193, 196, 200, 203, 206, 210, 213, 216, 219, 223, 226, 229, 232, 236, 239, 242, 245, 249, 252, 255, 259, 262, 265, 268, 272, 275, 278, 281, 285, 288, 291, 294, 298, 301, 304, 307, 311, 314, 317, 321, 324, 327, 330, 334, 337, 340, 343, 347, 350],
        BaseAttributes: {
            39: {
                BaseValue: 8.350515463917557,
                AddValue: .8350515463917522
            },
            40: {
                BaseValue: 14.7422680412371,
                AddValue: 1.2742688828108597
            },
            41: {
                BaseValue: 24.58762886597939,
                AddValue: 1.708920681674737
            },
            42: {
                BaseValue: 10.618556701030965,
                AddValue: 1.0618556701030923
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    29: {
        StrId: "chr_0003_endminf",
        NameHash: "-2349442812164400839",
        Rarity: 6,
        Element: "Physical",
        Profession: "GUARD",
        WeaponType: "Sword",
        MainAttrId: 40,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0003_endminf_5: {
                40: 15
            },
            chr_0003_endminf_7: {
                40: 20
            },
            chr_0003_endminf_3: {
                40: 15
            },
            chr_0003_endminf_1: {
                40: 10
            }
        },
        SkillInfoMap: {
            46: {
                Icon: "/ui/ef/skillicon/icon_skill_endmin_01.png",
                Element: "Physical"
            },
            47: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_endmin_01.png",
                Element: "Physical"
            },
            48: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_endmin_01.png",
                Element: "Physical"
            },
            45: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0003_endminf_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_endminm_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0003_endminf_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_endminm_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0003_endminf_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_endminm_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0003_endminf_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_endminm_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 4,
            Attrs: {
                1: {
                    Value: .1,
                    Formula: "BaseMultiplier"
                },
                60: {
                    Value: -.1,
                    Formula: "BaseAddition"
                },
                40: {
                    Value: 25,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 40, 43, 46, 49, 53, 56, 59, 62, 66, 69, 72, 75, 79, 82, 85, 88, 92, 95, 98, 101, 105, 108, 111, 114, 118, 121, 124, 127, 131, 134, 137, 140, 144, 147, 150, 153, 157, 160, 163, 166, 170, 173, 176, 179, 183, 186, 189, 192, 196, 199, 202, 205, 209, 212, 215, 218, 222, 225, 228, 231, 235, 238, 241, 244, 248, 251, 254, 257, 261, 264, 267, 270, 274, 277, 280, 283, 287, 290, 293, 296, 300, 303, 306, 309, 313, 316, 319, 322, 326, 329, 332, 335, 339, 342, 345, 348],
        BaseAttributes: {
            39: {
                BaseValue: 14.7422680412371,
                AddValue: 1.224279402482646
            },
            40: {
                BaseValue: 14.226804123711345,
                AddValue: 1.4226804123711387
            },
            41: {
                BaseValue: 9.793814432989725,
                AddValue: .9793814432989686
            },
            42: {
                BaseValue: 10.824742268041275,
                AddValue: 1.0824742268041232
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    30: {
        StrId: "chr_0019_karin",
        NameHash: "-1652352317843725885",
        Rarity: 4,
        Element: "Fire",
        Profession: "VANGUARD",
        WeaponType: "Sword",
        MainAttrId: 40,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0019_karin_1: {
                40: 10
            },
            chr_0019_karin_5: {
                40: 15
            },
            chr_0019_karin_3: {
                40: 15
            },
            chr_0019_karin_7: {
                40: 20
            }
        },
        SkillInfoMap: {
            68: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_karin_01.png",
                Element: "Physical"
            },
            65: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            },
            66: {
                Icon: "/ui/ef/skillicon/icon_skill_karin_01.png",
                Element: "Fire"
            },
            67: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_karin_01.png",
                Element: "Fire"
            }
        },
        NodeSkillMap: {
            chr_0019_karin_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_karin_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0019_karin_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_karin_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0019_karin_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_power_consume.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0019_karin_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_power_consume.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0019_karin_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_karin_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0019_karin_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0019_karin_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 2,
                Index: 2,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                40: {
                    Value: 10,
                    Formula: "BaseAddition"
                },
                41: {
                    Value: 10,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 40, 43, 46, 49, 53, 56, 59, 62, 66, 69, 72, 75, 79, 82, 85, 88, 92, 95, 98, 101, 105, 108, 111, 114, 118, 121, 124, 127, 131, 134, 137, 140, 144, 147, 150, 153, 157, 160, 163, 166, 170, 173, 176, 179, 183, 186, 189, 192, 196, 199, 202, 205, 209, 212, 215, 218, 222, 225, 228, 231, 235, 238, 241, 244, 248, 251, 254, 257, 261, 264, 267, 270, 274, 277, 280, 283, 287, 290, 293, 296, 300, 303, 306, 309, 313, 316, 319, 322, 326, 329, 332, 335, 339, 342, 345, 348],
        BaseAttributes: {
            39: {
                BaseValue: 13.402061855670151,
                AddValue: 1.090258783925941
            },
            40: {
                BaseValue: 15.154639175257735,
                AddValue: 1.4132127077635224
            },
            41: {
                BaseValue: 12.4742268041237,
                AddValue: 1.0599621291815724
            },
            42: {
                BaseValue: 9.27835051546395,
                AddValue: 1.1096149800126232
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    31: {
        StrId: "chr_0021_whiten",
        NameHash: "-7359346505174141947",
        Rarity: 4,
        Element: "Cryst",
        Profession: "GUARD",
        WeaponType: "Lance",
        MainAttrId: 42,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0021_whiten_5: {
                42: 15
            },
            chr_0021_whiten_7: {
                42: 20
            },
            chr_0021_whiten_1: {
                42: 10
            },
            chr_0021_whiten_3: {
                42: 15
            }
        },
        SkillInfoMap: {
            80: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_whiten_01.png",
                Element: "Physical"
            },
            78: {
                Icon: "/ui/ef/skillicon/icon_skill_whiten_01.png",
                Element: "Cryst"
            },
            79: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_whiten_01.png",
                Element: "Physical"
            },
            77: {
                Icon: "/ui/ef/skillicon/icon_attack_lance.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            fac_chr_0021_whiten_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0021_whiten_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_efficiency.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0021_whiten_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_whiten_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0021_whiten_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_whiten_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0021_whiten_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_efficiency.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0021_whiten_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_whiten_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0021_whiten_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_whiten_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0021_whiten_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 2,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 4,
            Attrs: {
                42: {
                    Value: 10,
                    Formula: "BaseAddition"
                },
                39: {
                    Value: 10,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 43, 46, 49, 52, 55, 58, 62, 65, 68, 71, 74, 77, 81, 84, 87, 90, 93, 96, 100, 103, 106, 109, 112, 115, 119, 122, 125, 128, 131, 134, 138, 141, 144, 147, 150, 153, 157, 160, 163, 166, 169, 172, 176, 179, 182, 185, 188, 191, 195, 198, 201, 204, 207, 210, 214, 217, 220, 223, 226, 229, 233, 236, 239, 242, 245, 248, 252, 255, 258, 261, 264, 267, 271, 274, 277, 280, 283, 286, 290, 293, 296, 299, 302, 305, 309, 312, 315, 318, 321, 324, 328, 331, 334, 337, 340],
        BaseAttributes: {
            39: {
                BaseValue: 13.04123711340205,
                AddValue: 1.0291815695350335
            },
            40: {
                BaseValue: 8.762886597938175,
                AddValue: 1.0012623606143485
            },
            41: {
                BaseValue: 14.123711340206237,
                AddValue: 1.0828950136755728
            },
            42: {
                BaseValue: 15.000000000000004,
                AddValue: 1.5340837365874234
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    32: {
        StrId: "chr_0022_bounda",
        NameHash: "4120402758683380662",
        Rarity: 4,
        Element: "Natural",
        Profession: "CASTER",
        WeaponType: "Pistol",
        MainAttrId: 40,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0022_bounda_1: {
                40: 10
            },
            chr_0022_bounda_3: {
                40: 15
            },
            chr_0022_bounda_5: {
                40: 15
            },
            chr_0022_bounda_7: {
                40: 20
            }
        },
        SkillInfoMap: {
            70: {
                Icon: "/ui/ef/skillicon/icon_skill_bounda_01.png",
                Element: "Natural"
            },
            72: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_bounda_01.png",
                Element: "Natural"
            },
            69: {
                Icon: "/ui/ef/skillicon/icon_attack_pistol.png",
                Element: "Natural"
            },
            71: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_bounda_01.png",
                Element: "Natural"
            }
        },
        NodeSkillMap: {
            fac_chr_0022_bounda_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0022_bounda_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_bounda_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0022_bounda_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_mineral.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0022_bounda_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_mineral.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0022_bounda_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_bounda_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0022_bounda_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_bounda_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0022_bounda_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_bounda_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0022_bounda_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 1,
            Attrs: {
                40: {
                    Value: 10,
                    Formula: "BaseAddition"
                },
                41: {
                    Value: 10,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 97, 101, 104, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 137, 140, 143, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 186, 189, 193, 196, 199, 202, 205, 208, 211, 214, 217, 220, 223, 226, 229, 232, 235, 238, 242, 245, 248, 251, 254, 257, 260, 263, 266, 269, 272, 275, 278, 281, 284, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327, 330],
        BaseAttributes: {
            39: {
                BaseValue: 14.02061855670108,
                AddValue: .8567220702714069
            },
            40: {
                BaseValue: 14.690721649484539,
                AddValue: 1.7247001893540976
            },
            41: {
                BaseValue: 12.4742268041237,
                AddValue: 1.1474437197559466
            },
            42: {
                BaseValue: 10.10309278350519,
                AddValue: .9194193141173991
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    33: {
        StrId: "chr_0023_antal",
        NameHash: "2232202019045239793",
        Rarity: 4,
        Element: "Pulse",
        Profession: "SUPPORTER",
        WeaponType: "Wand",
        MainAttrId: 41,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0023_antal_3: {
                41: 15
            },
            chr_0023_antal_1: {
                41: 10
            },
            chr_0023_antal_5: {
                41: 15
            },
            chr_0023_antal_7: {
                41: 20
            }
        },
        SkillInfoMap: {
            88: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_antal_01.png",
                Element: "Pulse"
            },
            85: {
                Icon: "/ui/ef/skillicon/icon_attack_funnel.png",
                Element: "Pulse"
            },
            87: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_antal_01.png",
                Element: "Pulse"
            },
            86: {
                Icon: "/ui/ef/skillicon/icon_skill_antal_01.png",
                Element: "Pulse"
            }
        },
        NodeSkillMap: {
            chr_0023_antal_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_antal_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0023_antal_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0023_antal_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_antal_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0023_antal_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0023_antal_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0023_antal_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_antal_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0023_antal_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_antal_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0023_antal_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 4,
            Attrs: {
                41: {
                    Value: 10,
                    Formula: "BaseAddition"
                },
                1: {
                    Value: .1,
                    Formula: "BaseMultiplier"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 186, 189, 192, 195, 198, 201, 204, 207, 210, 213, 216, 219, 222, 225, 228, 231, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324],
        BaseAttributes: {
            39: {
                BaseValue: 15.876288659793799,
                AddValue: 1.2751946139280488
            },
            40: {
                BaseValue: 9.48453608247426,
                AddValue: .8689248895434458
            },
            41: {
                BaseValue: 15.4639175257732,
                AddValue: 1.6827266989269987
            },
            42: {
                BaseValue: 9.793814432989725,
                AddValue: .8203240058910158
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    35: {
        StrId: "chr_0020_meurs",
        NameHash: "-494400192924640152",
        Rarity: 4,
        Element: "Physical",
        Profession: "DEFENDER",
        WeaponType: "Claymores",
        MainAttrId: 39,
        SubAttrId: 42,
        AttributeNodes: {
            chr_0020_meurs_3: {
                39: 15
            },
            chr_0020_meurs_7: {
                39: 20
            },
            chr_0020_meurs_1: {
                39: 10
            },
            chr_0020_meurs_5: {
                39: 15
            }
        },
        SkillInfoMap: {
            92: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_meurs_01.png",
                Element: "Physical"
            },
            90: {
                Icon: "/ui/ef/skillicon/icon_skill_meurs_01.png",
                Element: "Physical"
            },
            91: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_meurs_01.png",
                Element: "Physical"
            },
            89: {
                Icon: "/ui/ef/skillicon/icon_attack_claym.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0020_meurs_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_meurs_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0020_meurs_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0020_meurs_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_meurs_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0020_meurs_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0020_meurs_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0020_meurs_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_meurs_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0020_meurs_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_meurs_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0020_meurs_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 2,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                3: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                42: {
                    Value: 10,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 79, 82, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118, 121, 124, 127, 130, 133, 136, 139, 142, 145, 148, 151, 154, 157, 160, 163, 166, 170, 173, 176, 179, 182, 185, 188, 191, 194, 197, 200, 203, 206, 209, 212, 215, 218, 221, 224, 227, 230, 233, 236, 239, 242, 245, 248, 251, 254, 257, 261, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327],
        BaseAttributes: {
            39: {
                BaseValue: 21.64948453608248,
                AddValue: 1.738901746265522
            },
            40: {
                BaseValue: 9.793814432989725,
                AddValue: .9793814432989686
            },
            41: {
                BaseValue: 8.762886597938175,
                AddValue: .876288659793814
            },
            42: {
                BaseValue: 11.45360824742267,
                AddValue: 1.0703766042499503
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    38: {
        StrId: "chr_9000_endmin",
        NameHash: "-7421751997530373346",
        Rarity: 6,
        Element: "Physical",
        Profession: "GUARD",
        WeaponType: "Sword",
        MainAttrId: 40,
        SubAttrId: 39,
        AttributeNodes: {
            chr_9000_endmin_1: {
                40: 10
            },
            chr_9000_endmin_3: {
                40: 15
            },
            chr_9000_endmin_5: {
                40: 15
            },
            chr_9000_endmin_7: {
                40: 20
            }
        },
        SkillInfoMap: {
            74: {
                Icon: "/ui/ef/skillicon/icon_skill_endmin_01.png",
                Element: "Physical"
            },
            75: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_endmin_01.png",
                Element: "Physical"
            },
            76: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_endmin_01.png",
                Element: "Physical"
            },
            73: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_9000_endmin_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_endminm_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_9000_endmin_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_endminm_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_9000_endmin_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_endminm_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_9000_endmin_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_endminm_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 4,
            Attrs: {
                1: {
                    Value: .1,
                    Formula: "BaseMultiplier"
                },
                60: {
                    Value: -.1,
                    Formula: "BaseAddition"
                },
                40: {
                    Value: 25,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 40, 43, 46, 49, 53, 56, 59, 62, 66, 69, 72, 75, 79, 82, 85, 88, 92, 95, 98, 101, 105, 108, 111, 114, 118, 121, 124, 127, 131, 134, 137, 140, 144, 147, 150, 153, 157, 160, 163, 166, 170, 173, 176, 179, 183, 186, 189, 192, 196, 199, 202, 205, 209, 212, 215, 218, 222, 225, 228, 231, 235, 238, 241, 244, 248, 251, 254, 257, 261, 264, 267, 270, 274, 277, 280, 283, 287, 290, 293, 296, 300, 303, 306, 309, 313, 316, 319, 322, 326, 329, 332, 335, 339, 342, 345, 348],
        BaseAttributes: {
            39: {
                BaseValue: 14.7422680412371,
                AddValue: 1.224279402482646
            },
            40: {
                BaseValue: 14.226804123711345,
                AddValue: 1.4226804123711387
            },
            41: {
                BaseValue: 9.793814432989725,
                AddValue: .9793814432989686
            },
            42: {
                BaseValue: 10.824742268041275,
                AddValue: 1.0824742268041232
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    40: {
        StrId: "chr_0024_deepfin",
        NameHash: "4730225086587248930",
        Rarity: 5,
        Element: "Cryst",
        Profession: "VANGUARD",
        WeaponType: "Sword",
        MainAttrId: 39,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0024_deepfin_7: {
                39: 20
            },
            chr_0024_deepfin_1: {
                39: 10
            },
            chr_0024_deepfin_3: {
                39: 15
            },
            chr_0024_deepfin_5: {
                39: 15
            }
        },
        SkillInfoMap: {
            82: {
                Icon: "/ui/ef/skillicon/icon_skill_deepfin_01.png",
                Element: "Physical"
            },
            84: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_deepfin_01.png",
                Element: "Physical"
            },
            81: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            },
            83: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_deepfin_01.png",
                Element: "Cryst"
            }
        },
        NodeSkillMap: {
            fac_chr_0024_deepfin_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0024_deepfin_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0024_deepfin_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_deepfin_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0024_deepfin_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0024_deepfin_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_deepfin_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            chr_0024_deepfin_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_deepfin_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0024_deepfin_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_physical_power.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            chr_0024_deepfin_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_deepfin_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                39: {
                    Value: 15,
                    Formula: "BaseAddition"
                },
                41: {
                    Value: 15,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 36, 39, 43, 46, 49, 52, 55, 58, 61, 64, 68, 71, 74, 77, 80, 83, 86, 90, 93, 96, 99, 102, 105, 108, 111, 115, 118, 121, 124, 127, 130, 133, 136, 140, 143, 146, 149, 152, 155, 158, 162, 165, 168, 171, 174, 177, 180, 183, 187, 190, 193, 196, 199, 202, 205, 209, 212, 215, 218, 221, 224, 227, 230, 234, 237, 240, 243, 246, 249, 252, 256, 259, 262, 265, 268, 271, 274, 277, 281, 284, 287, 290, 293, 296, 299, 303, 306, 309, 312, 315, 318, 321, 324, 328, 331, 334, 337],
        BaseAttributes: {
            39: {
                BaseValue: 20.10309278350516,
                AddValue: 1.5501788344203713
            },
            40: {
                BaseValue: 9.48453608247426,
                AddValue: .9711760993057011
            },
            41: {
                BaseValue: 13.6082474226804,
                AddValue: 1.2608457816116174
            },
            42: {
                BaseValue: 10.824742268041275,
                AddValue: .8893330528087519
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    41: {
        StrId: "chr_0028_wulfa",
        NameHash: "7395048666191119127",
        Rarity: 6,
        Element: "Physical",
        Profession: "GUARD",
        WeaponType: "Sword",
        MainAttrId: 40,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0028_wulfa_7: {
                40: 20
            },
            chr_0028_wulfa_5: {
                40: 15
            },
            chr_0028_wulfa_1: {
                40: 10
            },
            chr_0028_wulfa_3: {
                40: 15
            }
        },
        SkillInfoMap: {
            112: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_wulfa_01.png",
                Element: "Physical"
            },
            109: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            },
            111: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_wulfa_01.png",
                Element: "Fire"
            },
            110: {
                Icon: "/ui/ef/skillicon/icon_skill_wulfa_01.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            chr_0028_wulfa_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_wulfa_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0028_wulfa_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_efficiency.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0028_wulfa_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_power_consume.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0028_wulfa_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_efficiency.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0028_wulfa_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_wulfa_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0028_wulfa_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_wulfa_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0028_wulfa_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_power_consume.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0028_wulfa_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_wulfa_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                40: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                9: {
                    Value: .07,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 46, 50, 53, 56, 60, 63, 66, 70, 73, 76, 79, 83, 86, 89, 93, 96, 99, 103, 106, 109, 112, 116, 119, 122, 126, 129, 132, 136, 139, 142, 145, 149, 152, 155, 159, 162, 165, 168, 172, 175, 178, 182, 185, 188, 192, 195, 198, 201, 205, 208, 211, 215, 218, 221, 225, 228, 231, 234, 238, 241, 244, 248, 251, 254, 258, 261, 264, 267, 271, 274, 277, 281, 284, 287, 291, 294, 297, 300, 304, 307, 310, 314, 317, 320, 323, 327, 330, 333, 337, 340, 343, 347, 350, 353],
        BaseAttributes: {
            39: {
                BaseValue: 9.896907216,
                AddValue: .9896907212653061
            },
            40: {
                BaseValue: 23.19587629,
                AddValue: 1.723122238877551
            },
            41: {
                BaseValue: 14.06185567,
                AddValue: 1.168735535
            },
            42: {
                BaseValue: 9.072164948,
                AddValue: .9072164948163266
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3.5,
                AddValue: 0
            },
            12: {
                BaseValue: 6.5,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    42: {
        StrId: "chr_0026_lastrite",
        NameHash: "2211452327399978399",
        Rarity: 6,
        Element: "Cryst",
        Profession: "ASSAULT",
        WeaponType: "Claymores",
        MainAttrId: 39,
        SubAttrId: 42,
        AttributeNodes: {
            chr_0026_lastrite_1: {
                39: 10
            },
            chr_0026_lastrite_3: {
                39: 15
            },
            chr_0026_lastrite_5: {
                39: 15
            },
            chr_0026_lastrite_7: {
                39: 20
            }
        },
        SkillInfoMap: {
            93: {
                Icon: "/ui/ef/skillicon/icon_attack_claym.png",
                Element: "Cryst"
            },
            94: {
                Icon: "/ui/ef/skillicon/icon_skill_lastrite_01.png",
                Element: "Cryst"
            },
            95: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_lastrite_01.png",
                Element: "Cryst"
            },
            96: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_lastrite_01.png",
                Element: "Cryst"
            }
        },
        NodeSkillMap: {
            fac_chr_0026_lastrite_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            fac_chr_0026_lastrite_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_clue.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0026_lastrite_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_flower.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0026_lastrite_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_flower.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0026_lastrite_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_lastrite_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0026_lastrite_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_lastrite_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0026_lastrite_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_lastrite_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0026_lastrite_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_lastrite_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                39: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                53: {
                    Value: .1,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 44, 47, 50, 54, 57, 61, 64, 67, 71, 74, 78, 81, 84, 88, 91, 95, 98, 101, 105, 108, 112, 115, 118, 122, 125, 129, 132, 135, 139, 142, 145, 149, 152, 156, 159, 162, 166, 169, 173, 176, 179, 183, 186, 190, 193, 196, 200, 203, 207, 210, 213, 217, 220, 224, 227, 230, 234, 237, 241, 244, 247, 251, 254, 258, 261, 264, 268, 271, 275, 278, 281, 285, 288, 292, 295, 298, 302, 305, 309, 312, 315, 319, 322, 326, 329, 332, 336, 339, 342, 346, 349, 353, 356, 359, 363],
        BaseAttributes: {
            39: {
                BaseValue: 21.64948453608248,
                AddValue: 1.5003155901535923
            },
            40: {
                BaseValue: 8.762886597938175,
                AddValue: 1.072838207447927
            },
            41: {
                BaseValue: 9.48453608247426,
                AddValue: .9484536082474222
            },
            42: {
                BaseValue: 15.876288659793799,
                AddValue: 1.0502419524510866
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    43: {
        StrId: "chr_0029_pograni",
        NameHash: "8750064674695776697",
        Rarity: 6,
        Element: "Physical",
        Profession: "VANGUARD",
        WeaponType: "Sword",
        MainAttrId: 42,
        SubAttrId: 40,
        AttributeNodes: {
            chr_0029_pograni_5: {
                42: 15
            },
            chr_0029_pograni_7: {
                42: 20
            },
            chr_0029_pograni_3: {
                42: 15
            },
            chr_0029_pograni_1: {
                42: 10
            }
        },
        SkillInfoMap: {
            100: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_pograni_01.png",
                Element: "Physical"
            },
            97: {
                Icon: "/ui/ef/skillicon/icon_attack_sword.png",
                Element: "Physical"
            },
            98: {
                Icon: "/ui/ef/skillicon/icon_skill_pograni_01.png",
                Element: "Physical"
            },
            99: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_pograni_01.png",
                Element: "Physical"
            }
        },
        NodeSkillMap: {
            fac_chr_0029_pograni_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            fac_chr_0029_pograni_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0029_pograni_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_pograni_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0029_pograni_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_pograni_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0029_pograni_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0029_pograni_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0029_pograni_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_pograni_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            chr_0029_pograni_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_pograni_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                42: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                50: {
                    Value: .1,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 46, 50, 53, 56, 59, 63, 66, 69, 72, 76, 79, 82, 85, 89, 92, 95, 99, 102, 105, 108, 112, 115, 118, 121, 125, 128, 131, 134, 138, 141, 144, 148, 151, 154, 157, 161, 164, 167, 170, 174, 177, 180, 183, 187, 190, 193, 196, 200, 203, 206, 210, 213, 216, 219, 223, 226, 229, 232, 236, 239, 242, 245, 249, 252, 255, 259, 262, 265, 268, 272, 275, 278, 281, 285, 288, 291, 294, 298, 301, 304, 307, 311, 314, 317, 321, 324, 327, 330, 334, 337, 340, 343, 347, 350],
        BaseAttributes: {
            39: {
                BaseValue: 12.3711340206186,
                AddValue: .9985272459499258
            },
            40: {
                BaseValue: 13.6082474226804,
                AddValue: 1.0858826004628686
            },
            41: {
                BaseValue: 10.3092783505155,
                AddValue: .9741216074058484
            },
            42: {
                BaseValue: 20.10309278350516,
                AddValue: 1.7205975173574637
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 3,
                AddValue: 0
            },
            12: {
                BaseValue: 3,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    44: {
        StrId: "chr_0025_ardelia",
        NameHash: "-5102726507612351418",
        Rarity: 6,
        Element: "Natural",
        Profession: "SUPPORTER",
        WeaponType: "Wand",
        MainAttrId: 41,
        SubAttrId: 42,
        AttributeNodes: {
            chr_0025_ardelia_7: {
                41: 20
            },
            chr_0025_ardelia_3: {
                41: 15
            },
            chr_0025_ardelia_1: {
                41: 10
            },
            chr_0025_ardelia_5: {
                41: 15
            }
        },
        SkillInfoMap: {
            104: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_ardelia_01.png",
                Element: "Natural"
            },
            101: {
                Icon: "/ui/ef/skillicon/icon_attack_funnel.png",
                Element: "Natural"
            },
            102: {
                Icon: "/ui/ef/skillicon/icon_skill_ardelia_01.png",
                Element: "Natural"
            },
            103: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_ardelia_01.png",
                Element: "Natural"
            }
        },
        NodeSkillMap: {
            chr_0025_ardelia_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_ardelia_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            fac_chr_0025_ardelia_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_efficiency.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            chr_0025_ardelia_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_ardelia_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0025_ardelia_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_power_consume.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0025_ardelia_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_ardelia_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0025_ardelia_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_efficiency.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0025_ardelia_passive_skill_0_3: {
                Icon: "/ui/ef/icon_talent_ardelia_01.png",
                Level: 3,
                Index: 0,
                Type: 4
            },
            fac_chr_0025_ardelia_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_guestroom_power_consume.png",
                Level: 1,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 46, 50, 53, 56, 60, 63, 66, 70, 73, 76, 79, 83, 86, 89, 93, 96, 99, 103, 106, 109, 112, 116, 119, 122, 126, 129, 132, 136, 139, 142, 145, 149, 152, 155, 159, 162, 165, 168, 172, 175, 178, 182, 185, 188, 192, 195, 198, 201, 205, 208, 211, 215, 218, 221, 225, 228, 231, 234, 238, 241, 244, 248, 251, 254, 258, 261, 264, 267, 271, 274, 277, 281, 284, 287, 291, 294, 297, 300, 304, 307, 310, 314, 317, 320, 323, 327, 330, 333, 337, 340, 343, 347, 350, 353],
        BaseAttributes: {
            39: {
                BaseValue: 9.793814432989725,
                AddValue: 1.149800126236061
            },
            40: {
                BaseValue: 9.48453608247426,
                AddValue: .9484536082474222
            },
            41: {
                BaseValue: 20.10309278350516,
                AddValue: 1.4138438880706967
            },
            42: {
                BaseValue: 15.876288659793799,
                AddValue: 1.1502209131075145
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    45: {
        StrId: "chr_0027_tangtang",
        NameHash: "-558922159116356568",
        Rarity: 6,
        Element: "Cryst",
        Profession: "CASTER",
        WeaponType: "Pistol",
        MainAttrId: 40,
        SubAttrId: 39,
        AttributeNodes: {
            chr_0027_tangtang_5: {
                40: 15
            },
            chr_0027_tangtang_7: {
                40: 20
            },
            chr_0027_tangtang_1: {
                40: 10
            },
            chr_0027_tangtang_3: {
                40: 15
            }
        },
        SkillInfoMap: {
            116: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_tangtang_01.png",
                Element: "Cryst"
            },
            113: {
                Icon: "/ui/ef/skillicon/icon_attack_pistol.png",
                Element: "Cryst"
            },
            115: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_tangtang_01.png",
                Element: "Cryst"
            },
            114: {
                Icon: "/ui/ef/skillicon/icon_skill_tangtang_01.png",
                Element: "Cryst"
            }
        },
        NodeSkillMap: {
            fac_chr_0027_tangtang_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0027_tangtang_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_flower.png",
                Level: 1,
                Index: 3,
                Type: 5
            },
            chr_0027_tangtang_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_tangtang_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            fac_chr_0027_tangtang_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_power_consume.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0027_tangtang_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_tangtang_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0027_tangtang_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_plant_flower.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            chr_0027_tangtang_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_tangtang_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0027_tangtang_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_tangtang_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                40: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                53: {
                    Value: .1,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 46, 50, 53, 56, 59, 63, 66, 69, 72, 76, 79, 82, 85, 89, 92, 95, 99, 102, 105, 108, 112, 115, 118, 121, 125, 128, 131, 134, 138, 141, 144, 148, 151, 154, 157, 161, 164, 167, 170, 174, 177, 180, 183, 187, 190, 193, 196, 200, 203, 206, 210, 213, 216, 219, 223, 226, 229, 232, 236, 239, 242, 245, 249, 252, 255, 259, 262, 265, 268, 272, 275, 278, 281, 285, 288, 291, 294, 298, 301, 304, 307, 311, 314, 317, 321, 324, 327, 330, 334, 337, 340, 343, 347, 350],
        BaseAttributes: {
            39: {
                BaseValue: 13.60824742,
                AddValue: 1.2358510416326531
            },
            40: {
                BaseValue: 23.50515464,
                AddValue: 1.7540500740816327
            },
            41: {
                BaseValue: 8.865979381,
                AddValue: .8638754471326531
            },
            42: {
                BaseValue: 10.30927835,
                AddValue: 1.0309278352040816
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 7.9,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    },
    46: {
        StrId: "chr_0030_zhuangfy",
        NameHash: "-5918768875146078054",
        Rarity: 6,
        Element: "Pulse",
        Profession: "ASSAULT",
        WeaponType: "Wand",
        MainAttrId: 42,
        SubAttrId: 41,
        AttributeNodes: {
            chr_0030_zhuangfy_1: {
                42: 10
            },
            chr_0030_zhuangfy_3: {
                42: 15
            },
            chr_0030_zhuangfy_5: {
                42: 15
            },
            chr_0030_zhuangfy_7: {
                42: 20
            }
        },
        SkillInfoMap: {
            107: {
                Icon: "/ui/ef/skillicon/icon_ultimate_skill_zhuangfy_01.png",
                Element: "Pulse"
            },
            108: {
                Icon: "/ui/ef/skillicon/icon_combo_skill_zhuangfy_01.png",
                Element: "Pulse"
            },
            105: {
                Icon: "/ui/ef/skillicon/icon_attack_funnel.png",
                Element: "Pulse"
            },
            106: {
                Icon: "/ui/ef/skillicon/icon_skill_zhuangfy_01.png",
                Element: "Pulse"
            }
        },
        NodeSkillMap: {
            chr_0030_zhuangfy_passive_skill_0_2: {
                Icon: "/ui/ef/icon_talent_zhuangfy_01.png",
                Level: 2,
                Index: 0,
                Type: 4
            },
            fac_chr_0030_zhuangfy_0_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 2,
                Index: 2,
                Type: 5
            },
            chr_0030_zhuangfy_passive_skill_1_2: {
                Icon: "/ui/ef/icon_talent_zhuangfy_02.png",
                Level: 2,
                Index: 1,
                Type: 4
            },
            chr_0030_zhuangfy_passive_skill_0_1: {
                Icon: "/ui/ef/icon_talent_zhuangfy_01.png",
                Level: 1,
                Index: 0,
                Type: 4
            },
            chr_0030_zhuangfy_passive_skill_1_1: {
                Icon: "/ui/ef/icon_talent_zhuangfy_02.png",
                Level: 1,
                Index: 1,
                Type: 4
            },
            fac_chr_0030_zhuangfy_1_2: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 2,
                Index: 3,
                Type: 5
            },
            fac_chr_0030_zhuangfy_0_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_power_consume.png",
                Level: 1,
                Index: 2,
                Type: 5
            },
            fac_chr_0030_zhuangfy_1_1: {
                Icon: "/ui/ef/spaceshipskillicon/facskill_spaceship_manufacture_efficiency.png",
                Level: 1,
                Index: 3,
                Type: 5
            }
        },
        PotAttributes: [{
            Level: 2,
            Attrs: {
                42: {
                    Value: 20,
                    Formula: "BaseAddition"
                },
                32: {
                    Value: .15,
                    Formula: "BaseAddition"
                }
            }
        }],
        BaseHpByLevel: [500, 556, 612, 668, 724, 781, 837, 893, 949, 1005, 1061, 1117, 1173, 1230, 1286, 1342, 1398, 1454, 1510, 1566, 1622, 1679, 1735, 1791, 1847, 1903, 1959, 2015, 2071, 2128, 2184, 2240, 2296, 2352, 2408, 2464, 2520, 2577, 2633, 2689, 2745, 2801, 2857, 2913, 2969, 3026, 3082, 3138, 3194, 3250, 3306, 3362, 3418, 3474, 3531, 3587, 3643, 3699, 3755, 3811, 3867, 3923, 3980, 4036, 4092, 4148, 4204, 4260, 4316, 4372, 4429, 4485, 4541, 4597, 4653, 4709, 4765, 4821, 4878, 4934, 4990, 5046, 5102, 5158, 5214, 5270, 5327, 5383, 5439, 5495, 5551, 5607, 5663, 5719, 5776, 5832, 5888, 5944, 6e3],
        BaseAtkByLevel: [30, 33, 37, 40, 43, 47, 50, 53, 57, 60, 63, 67, 70, 73, 77, 80, 83, 87, 90, 93, 97, 100, 103, 107, 110, 113, 117, 120, 123, 127, 130, 133, 137, 140, 143, 147, 150, 153, 157, 160, 163, 167, 170, 173, 177, 180, 183, 187, 190, 193, 197, 200, 203, 207, 210, 213, 217, 220, 223, 227, 230, 233, 236, 240, 243, 246, 250, 253, 256, 260, 263, 266, 270, 273, 276, 280, 283, 286, 290, 293, 296, 300, 303, 306, 310, 313, 316, 320, 323, 326, 330, 333, 336, 340, 343, 346, 350, 353, 356],
        BaseAttributes: {
            39: {
                BaseValue: 10.000000000000036,
                AddValue: .9999999999999994
            },
            40: {
                BaseValue: 10.000000000000036,
                AddValue: .9999999999999994
            },
            41: {
                BaseValue: 17.0103092783505,
                AddValue: 1.2011361245529175
            },
            42: {
                BaseValue: 24.74226804123712,
                AddValue: 1.7925520723753476
            },
            49: {
                BaseValue: 1,
                AddValue: .00510204081632653
            },
            25: {
                BaseValue: 1,
                AddValue: .002551020408163265
            },
            4: {
                BaseValue: 1,
                AddValue: 0
            },
            5: {
                BaseValue: 1,
                AddValue: 0
            },
            6: {
                BaseValue: 1,
                AddValue: 0
            },
            7: {
                BaseValue: 1,
                AddValue: 0
            },
            48: {
                BaseValue: 1,
                AddValue: 0
            },
            60: {
                BaseValue: 1,
                AddValue: 0
            },
            8: {
                BaseValue: 1,
                AddValue: 0
            },
            9: {
                BaseValue: .05,
                AddValue: 0
            },
            90: {
                BaseValue: 10,
                AddValue: 0
            },
            12: {
                BaseValue: 10,
                AddValue: 0
            },
            15: {
                BaseValue: 1,
                AddValue: 0
            },
            11: {
                BaseValue: 1,
                AddValue: 0
            }
        }
    }
}
  , s1 = {
    897: {
        Rarity: 4,
        NameHash: "-2019552733507290551",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0001.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1248, 1264, 2201]
    },
    1608: {
        Rarity: 3,
        NameHash: "7335365171316261327",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0001.png",
        LevelTemplateId: "weapon_upgrade_curve_3star_1",
        BreakthroughTemplateId: "weapon_breakthrough_3star_D_2",
        TalentTemplateId: "wpn_potential_3star",
        SkillList: [2301, 2207]
    },
    1776: {
        Rarity: 4,
        NameHash: "783077045341572465",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0003.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1244, 1264, 2209]
    },
    1777: {
        Rarity: 5,
        NameHash: "-5407485926004336253",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0004.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2443, 2447, 2268]
    },
    1778: {
        Rarity: 5,
        NameHash: "2184740646294663472",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0006.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2439, 2452, 2225]
    },
    1779: {
        Rarity: 5,
        NameHash: "4071437936762064420",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0005.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2439, 2455, 2219]
    },
    1780: {
        Rarity: 5,
        NameHash: "-1170822565033827697",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0007.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2443, 2456, 2226]
    },
    1781: {
        Rarity: 5,
        NameHash: "-6927181514487965292",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0005.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2443, 2444, 2217]
    },
    1782: {
        Rarity: 5,
        NameHash: "3791256304442110299",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0006.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2442, 2447, 2239]
    },
    1783: {
        Rarity: 4,
        NameHash: "8822408314463642803",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0008.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1246, 1264, 2205]
    },
    1784: {
        Rarity: 6,
        NameHash: "-6946349366864208445",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0007.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1243, 1255, 2250]
    },
    1785: {
        Rarity: 6,
        NameHash: "7771444582359825028",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0006.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1255, 2243]
    },
    1786: {
        Rarity: 5,
        NameHash: "-7538706656137713848",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0007.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2442, 2456, 2224]
    },
    1787: {
        Rarity: 3,
        NameHash: "-1905022870455162201",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0009.png",
        LevelTemplateId: "weapon_upgrade_curve_3star_1",
        BreakthroughTemplateId: "weapon_breakthrough_3star_A_1",
        TalentTemplateId: "wpn_potential_3star",
        SkillList: [2301, 2206]
    },
    1788: {
        Rarity: 3,
        NameHash: "-8977995465513072192",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0003.png",
        LevelTemplateId: "weapon_upgrade_curve_3star_1",
        BreakthroughTemplateId: "weapon_breakthrough_3star_B_2",
        TalentTemplateId: "wpn_potential_3star",
        SkillList: [2301, 2210]
    },
    1789: {
        Rarity: 6,
        NameHash: "-8252975117473196252",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0008.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1243, 1261, 2244]
    },
    1790: {
        Rarity: 6,
        NameHash: "-4436135919595349462",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0010.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1241, 1258, 2220]
    },
    1791: {
        Rarity: 6,
        NameHash: "5958661335505510863",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0009.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1247, 1263, 2229]
    },
    1792: {
        Rarity: 5,
        NameHash: "-7724333490536579654",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0012.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2441, 2451, 2274]
    },
    1793: {
        Rarity: 4,
        NameHash: "-6068143146164217015",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0003.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1242, 1250, 2204]
    },
    1794: {
        Rarity: 5,
        NameHash: "1260800784666033234",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0004.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2441, 2456, 2218]
    },
    1795: {
        Rarity: 3,
        NameHash: "-5357033486558439887",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0002.png",
        LevelTemplateId: "weapon_upgrade_curve_3star_1",
        BreakthroughTemplateId: "weapon_breakthrough_3star_C_1",
        TalentTemplateId: "wpn_potential_3star",
        SkillList: [2301, 2202]
    },
    1796: {
        Rarity: 6,
        NameHash: "-7407708142202564701",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0010.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 2253, 2228]
    },
    1797: {
        Rarity: 6,
        NameHash: "-1109747167756492602",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0006.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.03",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1247, 1249, 2237]
    },
    1798: {
        Rarity: 6,
        NameHash: "-4688376393957009563",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0005.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1247, 1252, 2255]
    },
    1799: {
        Rarity: 5,
        NameHash: "-507430032526329009",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0011.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2441, 2456, 2223]
    },
    1800: {
        Rarity: 6,
        NameHash: "1551839587735379560",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0006.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.98",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1257, 2271]
    },
    1801: {
        Rarity: 4,
        NameHash: "6678494521303129225",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0003.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1246, 1250, 2203]
    },
    1802: {
        Rarity: 4,
        NameHash: "-4609112903594886248",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0009.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1246, 1256, 2199]
    },
    1803: {
        Rarity: 4,
        NameHash: "-5056931015556203329",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0008.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1242, 1259, 2211]
    },
    1804: {
        Rarity: 6,
        NameHash: "-2984635888785852228",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0007.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1241, 1252, 2667]
    },
    1805: {
        Rarity: 4,
        NameHash: "-8961014337499272877",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0009.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1248, 1250, 2212]
    },
    1806: {
        Rarity: 3,
        NameHash: "7777877059457266142",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0010.png",
        LevelTemplateId: "weapon_upgrade_curve_3star_1",
        BreakthroughTemplateId: "weapon_breakthrough_3star_E_1",
        TalentTemplateId: "wpn_potential_3star",
        SkillList: [2301, 2200]
    },
    1808: {
        Rarity: 6,
        NameHash: "504161328765825530",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0012.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1249, 2234]
    },
    1809: {
        Rarity: 6,
        NameHash: "2231982712360458780",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0010.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1247, 1254, 2259]
    },
    1810: {
        Rarity: 5,
        NameHash: "-1726384258128348482",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0004.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2441, 2448, 2276]
    },
    1811: {
        Rarity: 6,
        NameHash: "-5040565645012012350",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0013.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 1258, 2235]
    },
    1812: {
        Rarity: 4,
        NameHash: "44802552962745243",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0002.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1248, 1250, 2208]
    },
    1813: {
        Rarity: 6,
        NameHash: "-5318664704038443001",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0008.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.01",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 1261, 2232]
    },
    1814: {
        Rarity: 6,
        NameHash: "-3001687498852588460",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0004.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.01",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 1249, 2242]
    },
    1815: {
        Rarity: 6,
        NameHash: "5227351883257320024",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0008.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.98",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1255, 2230]
    },
    1816: {
        Rarity: 6,
        NameHash: "-5486601487616328263",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0014.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.02",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 2253, 2236]
    },
    1817: {
        Rarity: 6,
        NameHash: "1973066223536924127",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0011.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 1261, 2233]
    },
    1818: {
        Rarity: 4,
        NameHash: "-5195668008198752422",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0003.png",
        LevelTemplateId: "weapon_upgrade_curve_4star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1244, 1250, 2198]
    },
    1819: {
        Rarity: 6,
        NameHash: "-8678598177954940370",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0011.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.01",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 1249, 2231]
    },
    2012: {
        Rarity: 6,
        NameHash: "-8631404038748537017",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0012.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.01",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1241, 1258, 2221]
    },
    2025: {
        Rarity: 6,
        NameHash: "237536856779192000",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0009.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1391, 1263, 2246]
    },
    3260: {
        Rarity: 5,
        NameHash: "-5095478813001721221",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0018.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2439, 2444, 2291]
    },
    3261: {
        Rarity: 5,
        NameHash: "-7362843078327416024",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0012.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2442, 2450, 2275]
    },
    3262: {
        Rarity: 5,
        NameHash: "8145093674632378709",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0015.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2439, 2455, 2269]
    },
    3263: {
        Rarity: 5,
        NameHash: "-7091197217007239969",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0014.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2443, 2454, 2306]
    },
    3264: {
        Rarity: 6,
        NameHash: "-8469995341331243725",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0011.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.01",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1260, 2272]
    },
    3265: {
        Rarity: 6,
        NameHash: "8266882546363894424",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0010.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.02",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1247, 1261, 2252]
    },
    3266: {
        Rarity: 6,
        NameHash: "5032726464451891463",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0013.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.02",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1243, 1249, 2251]
    },
    3267: {
        Rarity: 5,
        NameHash: "-1329975551577260521",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0019.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2439, 2444, 2260]
    },
    3268: {
        Rarity: 5,
        NameHash: "-4096224548721604136",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0015.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_C_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2441, 2451, 2298]
    },
    3269: {
        Rarity: 6,
        NameHash: "-1537494103470220508",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0013.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1247, 2449, 2273]
    },
    3270: {
        Rarity: 5,
        NameHash: "-7517728112529886151",
        WeaponType: "Lance",
        Icon: "/ui/ef/wpn_lance_0013.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2442, 2455, 2289]
    },
    3271: {
        Rarity: 5,
        NameHash: "642574601603060940",
        WeaponType: "Claymores",
        Icon: "/ui/ef/wpn_claym_0014.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2441, 2454, 2288]
    },
    3272: {
        Rarity: 6,
        NameHash: "8384767218372355757",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0016.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.01",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1249, 2227]
    },
    3273: {
        Rarity: 6,
        NameHash: "-7554233460720679627",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0021.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.01",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1241, 1249, 2222]
    },
    3274: {
        Rarity: 5,
        NameHash: "3039561516477140105",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0012.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2439, 2456, 2290]
    },
    3275: {
        Rarity: 5,
        NameHash: "-5682583205340247027",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0020.png",
        LevelTemplateId: "weapon_upgrade_curve_5star_1",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [2441, 2446, 2267]
    },
    3522: {
        Rarity: 6,
        NameHash: "7157814624270376536",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0017.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1253, 2913]
    },
    3524: {
        Rarity: 6,
        NameHash: "180869350560216944",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0022.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.02",
        BreakthroughTemplateId: "weapon_breakthrough_456star_E_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1241, 1261, 2665]
    },
    3525: {
        Rarity: 6,
        NameHash: "-5072318978327197490",
        WeaponType: "Sword",
        Icon: "/ui/ef/wpn_sword_0017.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_0.99",
        BreakthroughTemplateId: "weapon_breakthrough_456star_B_2",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1241, 1261, 2669]
    },
    3526: {
        Rarity: 6,
        NameHash: "-8484487047566132148",
        WeaponType: "Wand",
        Icon: "/ui/ef/wpn_funnel_0015.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.03",
        BreakthroughTemplateId: "weapon_breakthrough_456star_A_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1245, 1249, 2912]
    },
    3527: {
        Rarity: 6,
        NameHash: "67896441498939713",
        WeaponType: "Pistol",
        Icon: "/ui/ef/wpn_pistol_0011.png",
        LevelTemplateId: "weapon_upgrade_curve_6star_1.02",
        BreakthroughTemplateId: "weapon_breakthrough_456star_D_1",
        TalentTemplateId: "wpn_potential_456star",
        SkillList: [1241, 1249, 2668]
    }
}
  , O0 = {
    BreakSkillLevelBounds: {
        weapon_breakthrough_456star_A_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_3star_B_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_3star_E_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_456star_D_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_3star_B_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_3star_E_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_456star_D_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_456star_E_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_456star_E_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_3star_D_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_456star_B_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_3star_A_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_3star_A_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_3star_D_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_456star_B_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_3star_C_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_456star_C_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_456star_C_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        },
        weapon_breakthrough_3star_C_1: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 3,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 4,
                upperBound: 8
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 5,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        weapon_breakthrough_456star_A_2: {
            0: [{
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 3
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            1: [{
                lowerBound: 2,
                upperBound: 5
            }, {
                lowerBound: 1,
                upperBound: 4
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            2: [{
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 2,
                upperBound: 6
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            3: [{
                lowerBound: 3,
                upperBound: 8
            }, {
                lowerBound: 2,
                upperBound: 7
            }, {
                lowerBound: 1,
                upperBound: 4
            }],
            4: [{
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 3,
                upperBound: 9
            }, {
                lowerBound: 1,
                upperBound: 4
            }]
        }
    },
    LevelCurves: {
        "weapon_upgrade_curve_3star_1.05": [30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132, 135, 138, 141, 144, 147, 150, 153, 156, 159, 162, 165, 168, 171, 174, 177, 180, 183, 186, 189, 192, 195, 198, 201, 204, 207, 210, 213, 216, 219, 222, 225, 228, 231, 234, 237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 294, 297],
        weapon_upgrade_curve_4star_1: [34, 38, 41, 45, 48, 52, 55, 59, 62, 65, 69, 72, 76, 79, 83, 86, 90, 93, 96, 100, 103, 107, 110, 114, 117, 121, 124, 127, 131, 134, 138, 141, 145, 148, 152, 155, 158, 162, 165, 169, 172, 176, 179, 183, 186, 189, 193, 196, 200, 203, 207, 210, 214, 217, 220, 224, 227, 231, 234, 238, 241, 245, 248, 251, 255, 258, 262, 265, 269, 272, 276, 279, 282, 286, 289, 293, 296, 300, 303, 307, 310, 313, 317, 320, 324, 327, 331, 334, 338, 341],
        "weapon_upgrade_curve_4star_1.1": [38, 42, 45, 49, 53, 57, 61, 64, 68, 72, 76, 80, 83, 87, 91, 95, 99, 102, 106, 110, 114, 117, 121, 125, 129, 133, 136, 140, 144, 148, 152, 155, 159, 163, 167, 171, 174, 178, 182, 186, 189, 193, 197, 201, 205, 208, 212, 216, 220, 224, 227, 231, 235, 239, 242, 246, 250, 254, 258, 261, 265, 269, 273, 277, 280, 284, 288, 292, 296, 299, 303, 307, 311, 314, 318, 322, 326, 330, 333, 337, 341, 345, 349, 352, 356, 360, 364, 368, 371, 375],
        "weapon_upgrade_curve_6star_0.98": [49, 54, 59, 64, 69, 74, 78, 83, 88, 93, 98, 103, 108, 113, 118, 123, 127, 132, 137, 142, 147, 152, 157, 162, 167, 172, 176, 181, 186, 191, 196, 201, 206, 211, 216, 221, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 274, 279, 284, 289, 294, 299, 304, 309, 314, 319, 323, 328, 333, 338, 343, 348, 353, 358, 363, 368, 372, 377, 382, 387, 392, 397, 402, 407, 412, 417, 421, 426, 431, 436, 441, 446, 451, 456, 461, 466, 470, 475, 480, 485],
        "weapon_upgrade_curve_6star_0.99": [50, 54, 59, 64, 69, 74, 79, 84, 89, 94, 99, 104, 109, 114, 119, 124, 129, 134, 139, 144, 149, 153, 158, 163, 168, 173, 178, 183, 188, 193, 198, 203, 208, 213, 218, 223, 228, 233, 238, 243, 248, 252, 257, 262, 267, 272, 277, 282, 287, 292, 297, 302, 307, 312, 317, 322, 327, 332, 337, 342, 347, 351, 356, 361, 366, 371, 376, 381, 386, 391, 396, 401, 406, 411, 416, 421, 426, 431, 436, 441, 446, 450, 455, 460, 465, 470, 475, 480, 485, 490],
        "weapon_upgrade_curve_5star_0.9": [37, 41, 45, 49, 52, 56, 60, 63, 67, 71, 75, 78, 82, 86, 90, 93, 97, 101, 105, 108, 112, 116, 120, 123, 127, 131, 134, 138, 142, 146, 149, 153, 157, 161, 164, 168, 172, 176, 179, 183, 187, 190, 194, 198, 202, 205, 209, 213, 217, 220, 224, 228, 232, 235, 239, 243, 247, 250, 254, 258, 261, 265, 269, 273, 276, 280, 284, 288, 291, 295, 299, 303, 306, 310, 314, 317, 321, 325, 329, 332, 336, 340, 344, 347, 351, 355, 359, 362, 366, 370],
        "weapon_upgrade_curve_5star_0.97": [40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125, 129, 133, 137, 141, 145, 149, 153, 157, 161, 165, 169, 173, 177, 181, 185, 189, 193, 197, 201, 205, 209, 213, 217, 221, 225, 229, 233, 238, 242, 246, 250, 254, 258, 262, 266, 270, 274, 278, 282, 286, 290, 294, 298, 302, 306, 310, 314, 318, 322, 326, 330, 334, 338, 342, 346, 350, 354, 358, 362, 366, 370, 374, 378, 382, 386, 390, 394, 399],
        "weapon_upgrade_curve_5star_0.95": [39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 106, 110, 114, 118, 122, 126, 130, 134, 138, 142, 146, 150, 154, 158, 162, 166, 170, 173, 177, 181, 185, 189, 193, 197, 201, 205, 209, 213, 217, 221, 225, 229, 233, 237, 240, 244, 248, 252, 256, 260, 264, 268, 272, 276, 280, 284, 288, 292, 296, 300, 304, 308, 311, 315, 319, 323, 327, 331, 335, 339, 343, 347, 351, 355, 359, 363, 367, 371, 375, 378, 382, 386, 390],
        "weapon_upgrade_curve_5star_1.1": [46, 50, 55, 59, 64, 68, 73, 78, 82, 87, 91, 96, 100, 105, 110, 114, 119, 123, 128, 132, 137, 142, 146, 151, 155, 160, 164, 169, 173, 178, 183, 187, 192, 196, 201, 205, 210, 215, 219, 224, 228, 233, 237, 242, 247, 251, 256, 260, 265, 269, 274, 278, 283, 288, 292, 297, 301, 306, 310, 315, 320, 324, 329, 333, 338, 342, 347, 352, 356, 361, 365, 370, 374, 379, 383, 388, 393, 397, 402, 406, 411, 415, 420, 425, 429, 434, 438, 443, 447, 452],
        "weapon_upgrade_curve_3star_0.95": [27, 30, 33, 35, 38, 41, 43, 46, 49, 52, 54, 57, 60, 62, 65, 68, 71, 73, 76, 79, 81, 84, 87, 90, 92, 95, 98, 100, 103, 106, 109, 111, 114, 117, 120, 122, 125, 128, 130, 133, 136, 139, 141, 144, 147, 149, 152, 155, 158, 160, 163, 166, 168, 171, 174, 177, 179, 182, 185, 187, 190, 193, 196, 198, 201, 204, 206, 209, 212, 215, 217, 220, 223, 225, 228, 231, 234, 236, 239, 242, 244, 247, 250, 253, 255, 258, 261, 263, 266, 269],
        weapon_upgrade_curve_3star_1: [29, 31, 34, 37, 40, 43, 46, 49, 51, 54, 57, 60, 63, 66, 69, 71, 74, 77, 80, 83, 86, 89, 91, 94, 97, 100, 103, 106, 109, 111, 114, 117, 120, 123, 126, 129, 132, 134, 137, 140, 143, 146, 149, 152, 154, 157, 160, 163, 166, 169, 172, 174, 177, 180, 183, 186, 189, 192, 194, 197, 200, 203, 206, 209, 212, 214, 217, 220, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252, 254, 257, 260, 263, 266, 269, 272, 274, 277, 280, 283],
        "weapon_upgrade_curve_4star_0.9": [31, 34, 37, 40, 43, 47, 50, 53, 56, 59, 62, 65, 68, 71, 74, 78, 81, 84, 87, 90, 93, 96, 99, 102, 105, 109, 112, 115, 118, 121, 124, 127, 130, 133, 136, 140, 143, 146, 149, 152, 155, 158, 161, 164, 167, 171, 174, 177, 180, 183, 186, 189, 192, 195, 198, 202, 205, 208, 211, 214, 217, 220, 223, 226, 229, 233, 236, 239, 242, 245, 248, 251, 254, 257, 260, 264, 267, 270, 273, 276, 279, 282, 285, 288, 291, 295, 298, 301, 304, 307],
        "weapon_upgrade_curve_6star_1.02": [51, 56, 61, 66, 71, 77, 82, 87, 92, 97, 102, 107, 112, 117, 122, 128, 133, 138, 143, 148, 153, 158, 163, 168, 173, 179, 184, 189, 194, 199, 204, 209, 214, 219, 224, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 281, 286, 291, 296, 301, 306, 311, 316, 321, 326, 332, 337, 342, 347, 352, 357, 362, 367, 372, 377, 383, 388, 393, 398, 403, 408, 413, 418, 423, 428, 434, 439, 444, 449, 454, 459, 464, 469, 474, 479, 485, 490, 495, 500, 505],
        "weapon_upgrade_curve_5star_1.05": [44, 48, 52, 57, 61, 65, 70, 74, 78, 83, 87, 92, 96, 100, 105, 109, 113, 118, 122, 126, 131, 135, 139, 144, 148, 153, 157, 161, 166, 170, 174, 179, 183, 187, 192, 196, 200, 205, 209, 214, 218, 222, 227, 231, 235, 240, 244, 248, 253, 257, 261, 266, 270, 275, 279, 283, 288, 292, 296, 301, 305, 309, 314, 318, 322, 327, 331, 336, 340, 344, 349, 353, 357, 362, 366, 370, 375, 379, 383, 388, 392, 397, 401, 405, 410, 414, 418, 423, 427, 431],
        "weapon_upgrade_curve_6star_1.03": [52, 57, 62, 67, 72, 77, 82, 88, 93, 98, 103, 108, 113, 118, 124, 129, 134, 139, 144, 149, 155, 160, 165, 170, 175, 180, 185, 191, 196, 201, 206, 211, 216, 221, 227, 232, 237, 242, 247, 252, 258, 263, 268, 273, 278, 283, 288, 294, 299, 304, 309, 314, 319, 324, 330, 335, 340, 345, 350, 355, 361, 366, 371, 376, 381, 386, 391, 397, 402, 407, 412, 417, 422, 427, 433, 438, 443, 448, 453, 458, 464, 469, 474, 479, 484, 489, 494, 500, 505, 510],
        "weapon_upgrade_curve_4star_0.95": [33, 36, 39, 43, 46, 49, 52, 56, 59, 62, 65, 69, 72, 75, 79, 82, 85, 88, 92, 95, 98, 101, 105, 108, 111, 115, 118, 121, 124, 128, 131, 134, 137, 141, 144, 147, 151, 154, 157, 160, 164, 167, 170, 173, 177, 180, 183, 187, 190, 193, 196, 200, 203, 206, 209, 213, 216, 219, 223, 226, 229, 232, 236, 239, 242, 245, 249, 252, 255, 259, 262, 265, 268, 272, 275, 278, 281, 285, 288, 291, 295, 298, 301, 304, 308, 311, 314, 317, 321, 324],
        "weapon_upgrade_curve_6star_1.01": [51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101, 106, 111, 116, 121, 126, 131, 136, 141, 146, 152, 157, 162, 167, 172, 177, 182, 187, 192, 197, 202, 207, 212, 217, 222, 227, 232, 237, 242, 247, 253, 258, 263, 268, 273, 278, 283, 288, 293, 298, 303, 308, 313, 318, 323, 328, 333, 338, 343, 348, 354, 359, 364, 369, 374, 379, 384, 389, 394, 399, 404, 409, 414, 419, 424, 429, 434, 439, 444, 449, 455, 460, 465, 470, 475, 480, 485, 490, 495, 500],
        "weapon_upgrade_curve_5star_0.98": [41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 94, 98, 102, 106, 110, 114, 118, 122, 126, 130, 134, 138, 142, 146, 150, 155, 159, 163, 167, 171, 175, 179, 183, 187, 191, 195, 199, 203, 207, 211, 216, 220, 224, 228, 232, 236, 240, 244, 248, 252, 256, 260, 264, 268, 272, 277, 281, 285, 289, 293, 297, 301, 305, 309, 313, 317, 321, 325, 329, 333, 338, 342, 346, 350, 354, 358, 362, 366, 370, 374, 378, 382, 386, 390, 394, 399, 403],
        "weapon_upgrade_curve_5star_1.03": [43, 47, 51, 56, 60, 64, 68, 73, 77, 81, 85, 90, 94, 98, 103, 107, 111, 115, 120, 124, 128, 133, 137, 141, 145, 150, 154, 158, 162, 167, 171, 175, 180, 184, 188, 192, 197, 201, 205, 209, 214, 218, 222, 227, 231, 235, 239, 244, 248, 252, 256, 261, 265, 269, 274, 278, 282, 286, 291, 295, 299, 303, 308, 312, 316, 321, 325, 329, 333, 338, 342, 346, 351, 355, 359, 363, 368, 372, 376, 380, 385, 389, 393, 398, 402, 406, 410, 415, 419, 423],
        weapon_upgrade_curve_6star_1: [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335, 340, 345, 350, 355, 360, 365, 370, 375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 425, 430, 435, 440, 445, 450, 455, 460, 465, 470, 475, 480, 485, 490, 495],
        weapon_upgrade_curve_5star_1: [42, 46, 50, 54, 58, 62, 66, 71, 75, 79, 83, 87, 91, 95, 100, 104, 108, 112, 116, 120, 125, 129, 133, 137, 141, 145, 149, 154, 158, 162, 166, 170, 174, 178, 183, 187, 191, 195, 199, 203, 208, 212, 216, 220, 224, 228, 232, 237, 241, 245, 249, 253, 257, 261, 266, 270, 274, 278, 282, 286, 291, 295, 299, 303, 307, 311, 315, 320, 324, 328, 332, 336, 340, 344, 349, 353, 357, 361, 365, 369, 374, 378, 382, 386, 390, 394, 398, 403, 407, 411]
    },
    TalentSkillLevelBounds: {
        wpn_potential_3star: {
            1: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 1,
                upperBound: 1
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            2: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 2,
                upperBound: 2
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            3: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 3,
                upperBound: 3
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            4: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 4,
                upperBound: 4
            }, {
                lowerBound: 0,
                upperBound: 0
            }],
            5: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 5,
                upperBound: 5
            }, {
                lowerBound: 0,
                upperBound: 0
            }]
        },
        wpn_potential_456star: {
            1: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 1,
                upperBound: 1
            }],
            2: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 2,
                upperBound: 2
            }],
            3: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 3,
                upperBound: 3
            }],
            4: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 4,
                upperBound: 4
            }],
            5: [{
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 0,
                upperBound: 0
            }, {
                lowerBound: 5,
                upperBound: 5
            }]
        }
    }
}
  , N0 = {
    1039: {
        TagId: "",
        PropMap: {
            87: {
                Values: [30],
                Formula: "BaseAddition"
            }
        }
    },
    1040: {
        TagId: "",
        PropMap: {
            87: {
                Values: [30],
                Formula: "BaseAddition"
            }
        }
    },
    1041: {
        TagId: "",
        PropMap: {
            29: {
                Values: [.2],
                Formula: "BaseAddition"
            }
        }
    },
    1042: {
        TagId: "",
        PropMap: {
            2: {
                Values: [.08],
                Formula: "BaseMultiplier"
            }
        }
    },
    1066: {
        TagId: "",
        PropMap: {
            2: {
                Values: [.15],
                Formula: "BaseMultiplier"
            }
        }
    },
    1067: {
        TagId: "",
        PropMap: {
            47: {
                Values: [.85],
                Formula: "BaseFinalMultiplier"
            }
        }
    },
    1068: {
        TagId: "",
        PropMap: {
            9: {
                Values: [.05],
                Formula: "BaseAddition"
            }
        }
    },
    1069: {
        TagId: "",
        PropMap: {
            26: {
                Values: [.2],
                Formula: "BaseAddition"
            }
        }
    },
    1082: {
        TagId: "",
        PropMap: {
            40: {
                Values: [50],
                Formula: "BaseAddition"
            }
        }
    },
    1083: {
        TagId: "",
        PropMap: {
            39: {
                Values: [50],
                Formula: "BaseAddition"
            }
        }
    },
    1084: {
        TagId: "",
        PropMap: {
            42: {
                Values: [50],
                Formula: "BaseAddition"
            }
        }
    },
    1085: {
        TagId: "",
        PropMap: {
            41: {
                Values: [50],
                Formula: "BaseAddition"
            }
        }
    },
    1241: {
        TagId: "attr_agi",
        PropMap: {
            40: {
                Values: [20, 36, 52, 68, 84, 100, 116, 132, 156],
                Formula: "BaseAddition"
            }
        }
    },
    1242: {
        TagId: "attr_agi",
        PropMap: {
            40: {
                Values: [12, 21, 31, 40, 50, 60, 69, 79, 93],
                Formula: "BaseAddition"
            }
        }
    },
    1243: {
        TagId: "attr_str",
        PropMap: {
            39: {
                Values: [20, 36, 52, 68, 84, 100, 116, 132, 156],
                Formula: "BaseAddition"
            }
        }
    },
    1244: {
        TagId: "attr_str",
        PropMap: {
            39: {
                Values: [12, 21, 31, 40, 50, 60, 69, 79, 93],
                Formula: "BaseAddition"
            }
        }
    },
    1245: {
        TagId: "attr_will",
        PropMap: {
            42: {
                Values: [20, 36, 52, 68, 84, 100, 116, 132, 156],
                Formula: "BaseAddition"
            }
        }
    },
    1246: {
        TagId: "attr_will",
        PropMap: {
            42: {
                Values: [12, 21, 31, 40, 50, 60, 69, 79, 93],
                Formula: "BaseAddition"
            }
        }
    },
    1247: {
        TagId: "attr_wisd",
        PropMap: {
            41: {
                Values: [20, 36, 52, 68, 84, 100, 116, 132, 156],
                Formula: "BaseAddition"
            }
        }
    },
    1248: {
        TagId: "attr_wisd",
        PropMap: {
            41: {
                Values: [12, 21, 31, 40, 50, 60, 69, 79, 93],
                Formula: "BaseAddition"
            }
        }
    },
    1249: {
        TagId: "attr_atk",
        PropMap: {
            2: {
                Values: [.05, .09, .13, .17, .21, .25, .29, .33, .39],
                Formula: "BaseMultiplier"
            }
        }
    },
    1250: {
        TagId: "attr_atk",
        PropMap: {
            2: {
                Values: [.03, .054, .078, .102, .126, .15, .174, .198, .234],
                Formula: "BaseMultiplier"
            }
        }
    },
    1252: {
        TagId: "attr_icedam",
        PropMap: {
            53: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            }
        }
    },
    1253: {
        TagId: "attr_pulsedam",
        PropMap: {
            52: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            }
        }
    },
    1254: {
        TagId: "attr_firedam",
        PropMap: {
            51: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            }
        }
    },
    1255: {
        TagId: "attr_hp",
        PropMap: {
            1: {
                Values: [.1, .18, .26, .34, .42, .5, .58, .66, .78],
                Formula: "BaseMultiplier"
            }
        }
    },
    1256: {
        TagId: "attr_hp",
        PropMap: {
            1: {
                Values: [.06, .108, .156, .204, .252, .3, .348, .396, .468],
                Formula: "BaseMultiplier"
            }
        }
    },
    1257: {
        TagId: "attr_naturaldam",
        PropMap: {
            54: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            }
        }
    },
    1258: {
        TagId: "attr_phydam",
        PropMap: {
            50: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            }
        }
    },
    1259: {
        TagId: "attr_phydam",
        PropMap: {
            50: {
                Values: [.033333335, .06, .086666666, .11333334, .14, .16666667, .19333333, .22, .26],
                Formula: "BaseAddition"
            }
        }
    },
    1260: {
        TagId: "attr_usp",
        PropMap: {
            44: {
                Values: [.05952381, .10714286, .15476191, .20238096, .25, .29761904, .3452381, .39285713, .4642857],
                Formula: "BaseAddition"
            }
        }
    },
    1261: {
        TagId: "attr_crirate",
        PropMap: {
            9: {
                Values: [.025, .045, .065, .085, .105, .125, .145, .165, .195],
                Formula: "BaseAddition"
            }
        }
    },
    1263: {
        TagId: "attr_magicdam",
        PropMap: {
            53: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            },
            51: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            },
            52: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            },
            54: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            },
            55: {
                Values: [.055555556, .1, .14444445, .18888889, .23333333, .2777778, .32222223, .36666667, .43333334],
                Formula: "BaseAddition"
            }
        }
    },
    1264: {
        TagId: "attr_magicdam",
        PropMap: {
            53: {
                Values: [.033333335, .06, .086666666, .11333334, .14, .16666667, .19333333, .22, .26],
                Formula: "BaseAddition"
            },
            51: {
                Values: [.033333335, .06, .086666666, .11333334, .14, .16666667, .19333333, .22, .26],
                Formula: "BaseAddition"
            },
            52: {
                Values: [.033333335, .06, .086666666, .11333334, .14, .16666667, .19333333, .22, .26],
                Formula: "BaseAddition"
            },
            54: {
                Values: [.033333335, .06, .086666666, .11333334, .14, .16666667, .19333333, .22, .26],
                Formula: "BaseAddition"
            },
            55: {
                Values: [.033333335, .06, .086666666, .11333334, .14, .16666667, .19333333, .22, .26],
                Formula: "BaseAddition"
            }
        }
    },
    1391: {
        TagId: "attr_main",
        PropMap: {
            1e4: {
                Values: [17, 30, 44, 57, 71, 85, 98, 112, 132],
                Formula: "BaseAddition"
            }
        }
    },
    1911: {
        TagId: "",
        PropMap: {
            1: {
                Values: [500],
                Formula: "BaseFinalAddition"
            }
        }
    },
    1912: {
        TagId: "",
        PropMap: {
            1: {
                Values: [500],
                Formula: "BaseFinalAddition"
            }
        }
    },
    2071: {
        TagId: "",
        PropMap: {
            32: {
                Values: [.24],
                Formula: "BaseAddition"
            },
            33: {
                Values: [.24],
                Formula: "BaseAddition"
            },
            28: {
                Values: [.24],
                Formula: "BaseAddition"
            }
        }
    },
    2072: {
        TagId: "",
        PropMap: {
            2: {
                Values: [.15],
                Formula: "BaseMultiplier"
            }
        }
    },
    2073: {
        TagId: "",
        PropMap: {
            33: {
                Values: [.2],
                Formula: "BaseAddition"
            },
            32: {
                Values: [.2],
                Formula: "BaseAddition"
            },
            28: {
                Values: [.2],
                Formula: "BaseAddition"
            }
        }
    },
    2074: {
        TagId: "",
        PropMap: {
            44: {
                Values: [.2],
                Formula: "BaseAddition"
            }
        }
    },
    2075: {
        TagId: "",
        PropMap: {
            1: {
                Values: [1e3],
                Formula: "BaseFinalAddition"
            }
        }
    },
    2198: {
        TagId: "tactic",
        PropMap: {}
    },
    2199: {
        TagId: "smash",
        PropMap: {}
    },
    2200: {
        TagId: "force",
        PropMap: {
            2: {
                Values: [12, 14.4, 16.8, 19.2, 21.6, 24, 26.4, 28.8, 33.6],
                Formula: "BaseFinalAddition"
            }
        }
    },
    2201: {
        TagId: "spirit",
        PropMap: {}
    },
    2202: {
        TagId: "force",
        PropMap: {
            2: {
                Values: [12, 14.4, 16.8, 19.2, 21.6, 24, 26.4, 28.8, 33.6],
                Formula: "BaseFinalAddition"
            }
        }
    },
    2203: {
        TagId: "tactic",
        PropMap: {}
    },
    2204: {
        TagId: "spirit",
        PropMap: {}
    },
    2205: {
        TagId: "tactic",
        PropMap: {}
    },
    2206: {
        TagId: "force",
        PropMap: {
            2: {
                Values: [12, 14.4, 16.8, 19.2, 21.6, 24, 26.4, 28.8, 33.6],
                Formula: "BaseFinalAddition"
            }
        }
    },
    2207: {
        TagId: "force",
        PropMap: {
            2: {
                Values: [12, 14.4, 16.8, 19.2, 21.6, 24, 26.4, 28.8, 33.6],
                Formula: "BaseFinalAddition"
            }
        }
    },
    2208: {
        TagId: "tactic",
        PropMap: {}
    },
    2209: {
        TagId: "combo",
        PropMap: {}
    },
    2210: {
        TagId: "force",
        PropMap: {
            2: {
                Values: [12, 14.4, 16.8, 19.2, 21.6, 24, 26.4, 28.8, 33.6],
                Formula: "BaseFinalAddition"
            }
        }
    },
    2211: {
        TagId: "tactic",
        PropMap: {}
    },
    2212: {
        TagId: "combo",
        PropMap: {}
    },
    2217: {
        TagId: "ult",
        PropMap: {
            1: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseMultiplier"
            }
        }
    },
    2218: {
        TagId: "break",
        PropMap: {
            9: {
                Values: [.03, .036, .042, .048, .054, .06, .066, .072, .084],
                Formula: "BaseAddition"
            }
        }
    },
    2219: {
        TagId: "phyabn",
        PropMap: {
            2: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2220: {
        TagId: "phyabn",
        PropMap: {
            2: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseMultiplier"
            }
        }
    },
    2221: {
        TagId: "keyword",
        PropMap: {}
    },
    2222: {
        TagId: "magabn",
        PropMap: {
            87: {
                Values: [30, 36, 42, 48, 54, 60, 66, 72, 84],
                Formula: "BaseAddition"
            }
        }
    },
    2223: {
        TagId: "burst",
        PropMap: {
            1e4: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2224: {
        TagId: "spirit",
        PropMap: {
            1e4: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            },
            87: {
                Values: [25, 30, 35, 40, 45, 50, 55, 60, 70],
                Formula: "BaseAddition"
            }
        }
    },
    2225: {
        TagId: "magabn",
        PropMap: {
            9: {
                Values: [.03, .036, .042, .048, .054, .06, .066, .072, .084],
                Formula: "BaseAddition"
            }
        }
    },
    2226: {
        TagId: "spirit",
        PropMap: {
            2: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            },
            87: {
                Values: [25, 30, 35, 40, 45, 50, 55, 60, 70],
                Formula: "BaseAddition"
            }
        }
    },
    2227: {
        TagId: "tacafter",
        PropMap: {
            50: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseAddition"
            }
        }
    },
    2228: {
        TagId: "burst",
        PropMap: {
            10001: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseMultiplier"
            }
        }
    },
    2229: {
        TagId: "ult",
        PropMap: {
            9: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseAddition"
            }
        }
    },
    2230: {
        TagId: "heal",
        PropMap: {
            29: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseAddition"
            }
        }
    },
    2231: {
        TagId: "tactic",
        PropMap: {
            51: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            52: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            53: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            54: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            }
        }
    },
    2232: {
        TagId: "magabn",
        PropMap: {
            51: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            52: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            53: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            54: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            }
        }
    },
    2233: {
        TagId: "ult",
        PropMap: {}
    },
    2234: {
        TagId: "tacafter",
        PropMap: {
            2: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseMultiplier"
            }
        }
    },
    2235: {
        TagId: "break",
        PropMap: {
            2: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseMultiplier"
            }
        }
    },
    2236: {
        TagId: "magabn",
        PropMap: {
            51: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            52: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            53: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            54: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            }
        }
    },
    2237: {
        TagId: "ult",
        PropMap: {
            51: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseAddition"
            }
        }
    },
    2239: {
        TagId: "tactic",
        PropMap: {
            33: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseAddition"
            }
        }
    },
    2242: {
        TagId: "tactic",
        PropMap: {
            50: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseAddition"
            }
        }
    },
    2243: {
        TagId: "keyword",
        PropMap: {
            29: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseAddition"
            }
        }
    },
    2244: {
        TagId: "smash",
        PropMap: {}
    },
    2246: {
        TagId: "magabn",
        PropMap: {
            51: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            52: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            53: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            },
            54: {
                Values: [.12, .144, .168, .192, .216, .24, .264, .288, .336],
                Formula: "BaseAddition"
            }
        }
    },
    2250: {
        TagId: "heal",
        PropMap: {}
    },
    2251: {
        TagId: "burst",
        PropMap: {
            32: {
                Values: [.2, .24, .28, .32, .36, .4, .44, .48, .56],
                Formula: "BaseAddition"
            },
            33: {
                Values: [.2, .24, .28, .32, .36, .4, .44, .48, .56],
                Formula: "BaseAddition"
            },
            28: {
                Values: [.2, .24, .28, .32, .36, .4, .44, .48, .56],
                Formula: "BaseAddition"
            }
        }
    },
    2252: {
        TagId: "crit",
        PropMap: {
            53: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseAddition"
            }
        }
    },
    2253: {
        TagId: "attr_physpell",
        PropMap: {
            87: {
                Values: [10, 18, 26, 34, 42, 50, 58, 66, 78],
                Formula: "BaseAddition"
            }
        }
    },
    2255: {
        TagId: "magabn",
        PropMap: {
            9: {
                Values: [.035, .042, .049, .056, .063, .07, .077, .084, .098],
                Formula: "BaseAddition"
            }
        }
    },
    2259: {
        TagId: "magabn",
        PropMap: {
            2: {
                Values: [.07, .084, .098, .112, .126, .14, .154, .168, .196],
                Formula: "BaseMultiplier"
            }
        }
    },
    2260: {
        TagId: "tacafter",
        PropMap: {
            10001: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2267: {
        TagId: "tactic",
        PropMap: {
            2: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2268: {
        TagId: "magabn",
        PropMap: {
            87: {
                Values: [10, 12, 14, 16, 18, 20, 22, 24, 28],
                Formula: "BaseAddition"
            }
        }
    },
    2269: {
        TagId: "ult",
        PropMap: {
            28: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseAddition"
            }
        }
    },
    2271: {
        TagId: "tactic",
        PropMap: {
            2: {
                Values: [.07, .084, .098, .112, .126, .14, .154, .168, .196],
                Formula: "BaseMultiplier"
            }
        }
    },
    2272: {
        TagId: "combo",
        PropMap: {
            54: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "Addition"
            }
        }
    },
    2273: {
        TagId: "magabn",
        PropMap: {
            10001: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseMultiplier"
            }
        }
    },
    2274: {
        TagId: "heal",
        PropMap: {
            10001: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2275: {
        TagId: "heal",
        PropMap: {
            1e4: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2276: {
        TagId: "combo",
        PropMap: {
            32: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseAddition"
            }
        }
    },
    2288: {
        TagId: "break",
        PropMap: {
            87: {
                Values: [10, 12, 14, 16, 18, 20, 22, 24, 28],
                Formula: "BaseAddition"
            }
        }
    },
    2289: {
        TagId: "magabn",
        PropMap: {}
    },
    2290: {
        TagId: "burst",
        PropMap: {
            2: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2291: {
        TagId: "magabn",
        PropMap: {
            10001: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2298: {
        TagId: "keyword",
        PropMap: {
            10001: {
                Values: [.05, .06, .07, .08, .09, .1, .11, .12, .14],
                Formula: "BaseMultiplier"
            }
        }
    },
    2301: {
        TagId: "attr_main",
        PropMap: {
            1e4: {
                Values: [10, 18, 26, 34, 42, 51, 59, 67, 79],
                Formula: "BaseAddition"
            }
        }
    },
    2306: {
        TagId: "combo",
        PropMap: {
            1: {
                Values: [.1, .12, .14, .16, .18, .2, .22, .24, .28],
                Formula: "BaseMultiplier"
            }
        }
    },
    2439: {
        TagId: "attr_agi",
        PropMap: {
            40: {
                Values: [16, 28, 41, 54, 67, 80, 92, 105, 124],
                Formula: "BaseAddition"
            }
        }
    },
    2441: {
        TagId: "attr_str",
        PropMap: {
            39: {
                Values: [16, 28, 41, 54, 67, 80, 92, 105, 124],
                Formula: "BaseAddition"
            }
        }
    },
    2442: {
        TagId: "attr_will",
        PropMap: {
            42: {
                Values: [16, 28, 41, 54, 67, 80, 92, 105, 124],
                Formula: "BaseAddition"
            }
        }
    },
    2443: {
        TagId: "attr_wisd",
        PropMap: {
            41: {
                Values: [16, 28, 41, 54, 67, 80, 92, 105, 124],
                Formula: "BaseAddition"
            }
        }
    },
    2444: {
        TagId: "attr_atk",
        PropMap: {
            2: {
                Values: [.04, .072, .104, .136, .168, .2, .232, .264, .312],
                Formula: "BaseMultiplier"
            }
        }
    },
    2446: {
        TagId: "attr_icedam",
        PropMap: {
            53: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            }
        }
    },
    2447: {
        TagId: "attr_pulsedam",
        PropMap: {
            52: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            }
        }
    },
    2448: {
        TagId: "attr_firedam",
        PropMap: {
            51: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            }
        }
    },
    2449: {
        TagId: "attr_heal",
        PropMap: {
            29: {
                Values: [.05952381, .10714286, .15476191, .20238096, .25, .29761904, .3452381, .39285713, .4642857],
                Formula: "BaseAddition"
            }
        }
    },
    2450: {
        TagId: "attr_heal",
        PropMap: {
            29: {
                Values: [.04761905, .08571429, .123809524, .16190477, .2, .23809524, .2761905, .31428573, .37142858],
                Formula: "BaseAddition"
            }
        }
    },
    2451: {
        TagId: "attr_hp",
        PropMap: {
            1: {
                Values: [.08, .144, .208, .272, .336, .4, .464, .528, .624],
                Formula: "BaseMultiplier"
            }
        }
    },
    2452: {
        TagId: "attr_magicdam",
        PropMap: {
            53: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            },
            51: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            },
            52: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            },
            54: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            },
            55: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            }
        }
    },
    2454: {
        TagId: "attr_physpell",
        PropMap: {
            87: {
                Values: [8, 14, 20, 27, 33, 40, 46, 52, 62],
                Formula: "BaseAddition"
            }
        }
    },
    2455: {
        TagId: "attr_phydam",
        PropMap: {
            50: {
                Values: [.044444446, .08, .115555555, .15111111, .18666667, .22222222, .25777778, .29333332, .34666666],
                Formula: "BaseAddition"
            }
        }
    },
    2456: {
        TagId: "attr_usp",
        PropMap: {
            44: {
                Values: [.04761905, .08571429, .123809524, .16190477, .2, .23809524, .2761905, .31428573, .37142858],
                Formula: "BaseAddition"
            }
        }
    },
    2665: {
        TagId: "crit",
        PropMap: {
            2: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseMultiplier"
            }
        }
    },
    2667: {
        TagId: "tactic",
        PropMap: {
            2: {
                Values: [.07, .084, .098, .112, .126, .14, .154, .168, .196],
                Formula: "BaseMultiplier"
            }
        }
    },
    2668: {
        TagId: "burst",
        PropMap: {
            53: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseAddition"
            }
        }
    },
    2669: {
        TagId: "ult",
        PropMap: {
            2: {
                Values: [.07, .084, .098, .112, .126, .14, .154, .168, .196],
                Formula: "BaseMultiplier"
            }
        }
    },
    2846: {
        TagId: "",
        PropMap: {
            47: {
                Values: [.85],
                Formula: "BaseFinalMultiplier"
            }
        }
    },
    2847: {
        TagId: "",
        PropMap: {
            2: {
                Values: [.1],
                Formula: "BaseMultiplier"
            }
        }
    },
    2912: {
        TagId: "tactic",
        PropMap: {
            52: {
                Values: [.16, .192, .224, .256, .288, .32, .352, .384, .448],
                Formula: "BaseAddition"
            }
        }
    },
    2913: {
        TagId: "keyword",
        PropMap: {
            2: {
                Values: [.07, .084, .098, .112, .126, .14, .154, .168, .196],
                Formula: "BaseMultiplier"
            }
        }
    }
}
  , V0 = {
    TermNums: {
        42: {
            TermType: 1,
            TagId: "attr_agi",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "618525531035448622"
        },
        43: {
            TermType: 2,
            TagId: "attr_hp",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-6117555702377896924"
        },
        44: {
            TermType: 1,
            TagId: "attr_str",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-3695315761184824527"
        },
        49: {
            TermType: 2,
            TagId: "attr_atk",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-7621823970164654086"
        },
        50: {
            TermType: 2,
            TagId: "attr_crirate",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "7965435608132737754"
        },
        51: {
            TermType: 1,
            TagId: "attr_will",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "1677210984431925613"
        },
        53: {
            TermType: 2,
            TagId: "attr_phydam",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "6104225019296267130"
        },
        54: {
            TermType: 2,
            TagId: "attr_naturaldam",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "2830987437789703956"
        },
        55: {
            TermType: 2,
            TagId: "attr_pulsedam",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "1403731421098520645"
        },
        58: {
            TermType: 2,
            TagId: "attr_firedam",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-5343802871464601666"
        },
        63: {
            TermType: 3,
            TagId: "smash",
            TagIcon: "/ui/ef/itemicon/icon_smash.png",
            TagNameHash: "8516929077182091703"
        },
        64: {
            TermType: 3,
            TagId: "spirit",
            TagIcon: "/ui/ef/itemicon/icon_spirit.png",
            TagNameHash: "-3830975148475864038"
        },
        65: {
            TermType: 3,
            TagId: "tacafter",
            TagIcon: "/ui/ef/itemicon/icon_tacafter.png",
            TagNameHash: "-4954117345584935971"
        },
        66: {
            TermType: 3,
            TagId: "force",
            TagIcon: "/ui/ef/itemicon/icon_force.png",
            TagNameHash: "-8096686405280474233"
        },
        67: {
            TermType: 2,
            TagId: "attr_magicdam",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-7902866072207713679"
        },
        68: {
            TermType: 1,
            TagId: "attr_wisd",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-3168970582855925605"
        },
        69: {
            TermType: 3,
            TagId: "magabn",
            TagIcon: "/ui/ef/itemicon/icon_magabn.png",
            TagNameHash: "-2920864875609558632"
        },
        70: {
            TermType: 3,
            TagId: "ult",
            TagIcon: "/ui/ef/itemicon/icon_ult.png",
            TagNameHash: "-6805743900651681181"
        },
        72: {
            TermType: 3,
            TagId: "burst",
            TagIcon: "/ui/ef/itemicon/icon_burst.png",
            TagNameHash: "-898817599147833453"
        },
        73: {
            TermType: 3,
            TagId: "crit",
            TagIcon: "/ui/ef/itemicon/icon_crit.png",
            TagNameHash: "-5958662688507712294"
        },
        74: {
            TermType: 3,
            TagId: "phyabn",
            TagIcon: "/ui/ef/itemicon/icon_phyabn.png",
            TagNameHash: "-8030743302442077991"
        },
        76: {
            TermType: 2,
            TagId: "attr_icedam",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "3785849084286115810"
        },
        77: {
            TermType: 3,
            TagId: "heal",
            TagIcon: "/ui/ef/itemicon/icon_heal.png",
            TagNameHash: "3941348009204205064"
        },
        78: {
            TermType: 3,
            TagId: "tactic",
            TagIcon: "/ui/ef/itemicon/icon_tactic.png",
            TagNameHash: "-6775470065394008794"
        },
        79: {
            TermType: 2,
            TagId: "attr_usp",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-1559762980892459818"
        },
        80: {
            TermType: 3,
            TagId: "break",
            TagIcon: "/ui/ef/itemicon/icon_break.png",
            TagNameHash: "-2955380394353016630"
        },
        81: {
            TermType: 3,
            TagId: "combo",
            TagIcon: "/ui/ef/itemicon/icon_combo.png",
            TagNameHash: "553823228642190685"
        },
        83: {
            TermType: 1,
            TagId: "attr_main",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "-4674119795824731023"
        },
        85: {
            TermType: 3,
            TagId: "keyword",
            TagIcon: "/ui/ef/itemicon/icon_key.png",
            TagNameHash: "-3895520527121663973"
        },
        86: {
            TermType: 2,
            TagId: "attr_physpell",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "7713074992098148871"
        },
        87: {
            TermType: 2,
            TagId: "attr_heal",
            TagIcon: "/ui/ef/itemicon/icon_wpngem_00.png",
            TagNameHash: "481474268538502351"
        }
    },
    TemplateItems: {
        1770: {
            Icon: "/ui/ef/item_gem_rarity_2.png"
        },
        1068: {
            Icon: "/ui/ef/item_gem_rarity_2.png"
        },
        1066: {
            Icon: "/ui/ef/item_gem_rarity_3.png"
        },
        1069: {
            Icon: "/ui/ef/item_gem_rarity_4.png"
        },
        1070: {
            Icon: "/ui/ef/item_gem_rarity_5.png"
        }
    }
}
  , de = {
    Items: {
        2814: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_hand_02.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 17,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }]
        },
        2817: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_poise01_edc_04.png",
            SuitId: "suit_poise01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        2819: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_burst01_edc_02.png",
            SuitId: "suit_burst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 17,
                Formula: "BaseAddition",
                Values: [.27599999999999997, .3036, .33119999999999994, .35879999999999995]
            }]
        },
        2821: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_edc_03.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        2822: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_edc_03.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [31, 31, 31, 31]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.18571428571428572, .18571428571428572, .18571428571428572, .18571428571428572]
            }]
        },
        2823: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_hand_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [86, 94, 103, 111]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.45, .49500000000000005, .54, .5850000000000001]
            }]
        },
        2824: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_hand_03.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [12, 12, 12, 12]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [20, 20, 20, 20]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [13, 13, 13, 13]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.11, .11, .11, .11]
            }]
        },
        2826: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_agi01_body_01.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [28.8, 28.8, 28.8, 28.8]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [44, 44, 44, 44]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [29, 29, 29, 29]
            }, {
                AttrType: 2,
                Formula: "BaseFinalAddition",
                Values: [16.187704477740866, 16.187704477740866, 16.187704477740866, 16.187704477740866]
            }]
        },
        2832: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_will01_hand_01.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21.599999999999998, 21.599999999999998, 21.599999999999998, 21.599999999999998]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [33, 33, 33, 33]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.0875, .0875, .0875, .0875]
            }]
        },
        2834: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_usp01_edc_03.png",
            SuitId: "suit_usp01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [29.4, 29.4, 29.4, 29.4]
            }]
        },
        2835: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_hand_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [16.8, 16.8, 16.8, 16.8]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [28, 28, 28, 28]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [18, 18, 18, 18]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.15, .15, .15, .15]
            }]
        },
        2838: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_edc_03.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.294, .294, .294, .294]
            }]
        },
        2839: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_edc_01.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.19599999999999998, .19599999999999998, .19599999999999998, .19599999999999998]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.19599999999999998, .19599999999999998, .19599999999999998, .19599999999999998]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.19599999999999998, .19599999999999998, .19599999999999998, .19599999999999998]
            }]
        },
        2841: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_body_04.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.147, .147, .147, .147]
            }]
        },
        2843: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_edc_01.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [41.4, 45.54, 49.68, 53.82]
            }]
        },
        2844: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_hand_01.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        2845: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_pulse_cryst01_edc_03.png",
            SuitId: "suit_pulse_cryst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.5175, .56925, .6209999999999999, .67275]
            }]
        },
        2846: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_edc_01.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        2848: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_edc_04.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 61,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        2849: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_body_04.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.13799999999999998, .1518, .16559999999999997, .17939999999999998]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.13799999999999998, .1518, .16559999999999997, .17939999999999998]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.13799999999999998, .1518, .16559999999999997, .17939999999999998]
            }]
        },
        2850: {
            Rarity: 1,
            Icon: "/ui/ef/itemicon/item_equip_t0_parts_tundra01_body_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [8, 8, 8, 8]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [10, 10, 10, 10]
            }, {
                AttrType: 1,
                Formula: "BaseFinalAddition",
                Values: [46.3273721859878, 46.3273721859878, 46.3273721859878, 46.3273721859878]
            }]
        },
        2853: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_wisd01_body_01.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [28.8, 28.8, 28.8, 28.8]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [44, 44, 44, 44]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [29, 29, 29, 29]
            }, {
                AttrType: 2,
                Formula: "BaseFinalAddition",
                Values: [16.187704477740866, 16.187704477740866, 16.187704477740866, 16.187704477740866]
            }]
        },
        2854: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_edc_05.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        2855: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_pulse_cryst01_edc_02.png",
            SuitId: "suit_pulse_cryst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [41.4, 45.54, 49.68, 53.82]
            }]
        },
        2861: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_body_04.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        2863: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_str01_edc_02.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.21, .21, .21, .21]
            }]
        },
        2864: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_edc_05.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.27599999999999997, .3036, .33119999999999994, .35879999999999995]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.27599999999999997, .3036, .33119999999999994, .35879999999999995]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.27599999999999997, .3036, .33119999999999994, .35879999999999995]
            }]
        },
        2865: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_body_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [115, 126, 138, 149]
            }, {
                AttrType: 17,
                Formula: "BaseAddition",
                Values: [.144, .1584, .17279999999999998, .1872]
            }]
        },
        2866: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_parts_tundra01_edc_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.228, .228, .228, .228]
            }]
        },
        2869: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_hand_01.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [34.5, 37.95, 41.4, 44.85]
            }]
        },
        2870: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_edc_04.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        2871: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_edc_02.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        2874: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_hand_04.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [16.8, 16.8, 16.8, 16.8]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [28, 28, 28, 28]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [18, 18, 18, 18]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.15, .15, .15, .15]
            }]
        },
        2876: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_str01_body_01.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [28.8, 28.8, 28.8, 28.8]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [44, 44, 44, 44]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [29, 29, 29, 29]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.105, .105, .105, .105]
            }]
        },
        2879: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_edc_02.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 61,
                Formula: "BaseAddition",
                Values: [.294, .294, .294, .294]
            }]
        },
        2880: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_wisd01_edc_03.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.0525, .0525, .0525, .0525]
            }]
        },
        2883: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_usp01_edc_02.png",
            SuitId: "suit_usp01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 10001,
                Formula: "BaseMultiplier",
                Values: [.14701266544257816, .14701266544257816, .14701266544257816, .14701266544257816]
            }]
        },
        2884: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_body_03.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.05175, .056925, .062099999999999995, .067275]
            }]
        },
        2885: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_body_03.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.0875, .0875, .0875, .0875]
            }]
        },
        2887: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_body_01.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }]
        },
        2888: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_hand_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [49, 49, 49, 49]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 32, 32, 32]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.15476190476190477, .15476190476190477, .15476190476190477, .15476190476190477]
            }]
        },
        2889: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_agi01_edc_01.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.294, .294, .294, .294]
            }]
        },
        2890: {
            Rarity: 1,
            Icon: "/ui/ef/itemicon/item_equip_t0_parts_tundra01_body_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [8, 8, 8, 8]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [10, 10, 10, 10]
            }, {
                AttrType: 1,
                Formula: "BaseFinalAddition",
                Values: [46.3273721859878, 46.3273721859878, 46.3273721859878, 46.3273721859878]
            }]
        },
        2893: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_body_02.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.1035, .11385, .12419999999999999, .13455]
            }]
        },
        2895: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_agi01_hand_01.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21.599999999999998, 21.599999999999998, 21.599999999999998, 21.599999999999998]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [33, 33, 33, 33]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.09722222222222222, .09722222222222222, .09722222222222222, .09722222222222222]
            }]
        },
        2898: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_edc_04.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.10799999999999998, .11879999999999999, .12959999999999997, .1404]
            }]
        },
        2900: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_body_04.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        2902: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_stragi01_edc_01.png",
            SuitId: "suit_stragi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [8.4, 8.4, 8.4, 8.4]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [16, 16, 16, 16]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }]
        },
        2906: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_stragi01_edc_02.png",
            SuitId: "suit_stragi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [8.4, 8.4, 8.4, 8.4]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [16, 16, 16, 16]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.9250693802035153, .9250693802035153, .9250693802035153, .9250693802035153]
            }]
        },
        2908: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_str01_hand_01.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [46, 46, 46, 46]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.1225, .1225, .1225, .1225]
            }]
        },
        2910: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_str01_edc_01.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        2914: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_will01_body_01.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        2915: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_wisd01_edc_02.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.11666666666666667, .11666666666666667, .11666666666666667, .11666666666666667]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.11666666666666667, .11666666666666667, .11666666666666667, .11666666666666667]
            }]
        },
        2916: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_edc_01.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.828500414250207, .8145312372729494, .8010253123998718, .7879599716334411]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.828500414250207, .8145312372729494, .8010253123998718, .7879599716334411]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.828500414250207, .8145312372729494, .8010253123998718, .7879599716334411]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.828500414250207, .8145312372729494, .8010253123998718, .7879599716334411]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.828500414250207, .8145312372729494, .8010253123998718, .7879599716334411]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.828500414250207, .8145312372729494, .8010253123998718, .7879599716334411]
            }]
        },
        2918: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_wisdwill01_hand_01.png",
            SuitId: "suit_wisdwill01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [16.8, 16.8, 16.8, 16.8]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.135, .135, .135, .135]
            }]
        },
        2921: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_poise01_edc_01.png",
            SuitId: "suit_poise01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        2925: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_wisdwill01_edc_01.png",
            SuitId: "suit_wisdwill01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [8.4, 8.4, 8.4, 8.4]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [16, 16, 16, 16]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.162, .162, .162, .162]
            }]
        },
        2926: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_hand_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [49, 49, 49, 49]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 32, 32, 32]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.13, .13, .13, .13]
            }]
        },
        2927: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_body_03.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        2928: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_wisd01_edc_01.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.105, .105, .105, .105]
            }]
        },
        2929: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_body_02.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        2930: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_burst01_hand_01.png",
            SuitId: "suit_burst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        2931: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_body_02.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.147, .147, .147, .147]
            }]
        },
        2937: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_edc_01.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        2942: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_wisd01_hand_01.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21.599999999999998, 21.599999999999998, 21.599999999999998, 21.599999999999998]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [33, 33, 33, 33]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.09210526315789473, .09210526315789473, .09210526315789473, .09210526315789473]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.09210526315789473, .09210526315789473, .09210526315789473, .09210526315789473]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.09210526315789473, .09210526315789473, .09210526315789473, .09210526315789473]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.09210526315789473, .09210526315789473, .09210526315789473, .09210526315789473]
            }]
        },
        2943: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_edc_03.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.1035, .11385, .12419999999999999, .13455]
            }]
        },
        2944: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_usp02_body_01.png",
            SuitId: "suit_usp02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [20.7, 22.77, 24.84, 26.91]
            }]
        },
        2946: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_edc_03.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [41.4, 45.54, 49.68, 53.82]
            }]
        },
        2950: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_stragi01_body_01.png",
            SuitId: "suit_stragi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [22.400000000000002, 22.400000000000002, 22.400000000000002, 22.400000000000002]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.9610764055742431, .9610764055742431, .9610764055742431, .9610764055742431]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.9610764055742431, .9610764055742431, .9610764055742431, .9610764055742431]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.9610764055742431, .9610764055742431, .9610764055742431, .9610764055742431]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.9610764055742431, .9610764055742431, .9610764055742431, .9610764055742431]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.9610764055742431, .9610764055742431, .9610764055742431, .9610764055742431]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.9610764055742431, .9610764055742431, .9610764055742431, .9610764055742431]
            }]
        },
        2951: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_hand_01.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.345, .3795, .414, .44849999999999995]
            }]
        },
        2953: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_body_01.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }]
        },
        2954: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_edc_03.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        2956: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_edc_06.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.294, .294, .294, .294]
            }]
        },
        2957: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_hand_03.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        2967: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_edc_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [6, 6, 6, 6]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.066, .066, .066, .066]
            }]
        },
        2968: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_wisdwill01_edc_02.png",
            SuitId: "suit_wisdwill01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [8.4, 8.4, 8.4, 8.4]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [16, 16, 16, 16]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.162, .162, .162, .162]
            }]
        },
        2971: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_str01_edc_02.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.0735, .0735, .0735, .0735]
            }]
        },
        2972: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_edc_04.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        2973: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_edc_05.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.294, .294, .294, .294]
            }]
        },
        2978: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_hand_02.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.1725, .18975, .207, .22424999999999998]
            }]
        },
        2979: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_will01_body_01.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [28.8, 28.8, 28.8, 28.8]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [44, 44, 44, 44]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [29, 29, 29, 29]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.105, .105, .105, .105]
            }]
        },
        2981: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_body_04.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        2983: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_body_01.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        2984: {
            Rarity: 1,
            Icon: "/ui/ef/itemicon/item_equip_t0_parts_tundra01_hand_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [6, 6, 6, 6]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [11, 11, 11, 11]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [7, 7, 7, 7]
            }, {
                AttrType: 1,
                Formula: "BaseFinalAddition",
                Values: [77.21228697664634, 77.21228697664634, 77.21228697664634, 77.21228697664634]
            }]
        },
        2985: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_hand_01.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.345, .3795, .414, .44849999999999995]
            }]
        },
        2986: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_pulse_cryst01_hand_01.png",
            SuitId: "suit_pulse_cryst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        2991: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_hand_01.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.345, .3795, .414, .44849999999999995]
            }]
        },
        2994: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_wisdwill01_body_01.png",
            SuitId: "suit_wisdwill01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [22.400000000000002, 22.400000000000002, 22.400000000000002, 22.400000000000002]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.081, .081, .081, .081]
            }]
        },
        2997: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_body_03.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [22.400000000000002, 22.400000000000002, 22.400000000000002, 22.400000000000002]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [37, 37, 37, 37]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [25, 25, 25, 25]
            }, {
                AttrType: 2,
                Formula: "BaseFinalAddition",
                Values: [11.716709215321123, 11.716709215321123, 11.716709215321123, 11.716709215321123]
            }]
        },
        3e3: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_hand_02.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.43125, .47437500000000005, .5175, .560625]
            }]
        },
        3003: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_hand_02.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }]
        },
        3004: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_edc_04.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3006: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_edc_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [31, 31, 31, 31]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.8650519031141869, .8650519031141869, .8650519031141869, .8650519031141869]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.8650519031141869, .8650519031141869, .8650519031141869, .8650519031141869]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.8650519031141869, .8650519031141869, .8650519031141869, .8650519031141869]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.8650519031141869, .8650519031141869, .8650519031141869, .8650519031141869]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.8650519031141869, .8650519031141869, .8650519031141869, .8650519031141869]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.8650519031141869, .8650519031141869, .8650519031141869, .8650519031141869]
            }]
        },
        3007: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_body_02.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [20.7, 22.77, 24.84, 26.91]
            }]
        },
        3009: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_edc_03.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 1e4,
                Formula: "BaseMultiplier",
                Values: [.2070178350109774, .22771961851207514, .24842140201317287, .2691231855142706]
            }]
        },
        3010: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_body_04.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [22.400000000000002, 22.400000000000002, 22.400000000000002, 22.400000000000002]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [37, 37, 37, 37]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [25, 25, 25, 25]
            }, {
                AttrType: 2,
                Formula: "BaseFinalAddition",
                Values: [11.716709215321123, 11.716709215321123, 11.716709215321123, 11.716709215321123]
            }]
        },
        3011: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_edc_02.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3012: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_hand_01.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        3014: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_body_01.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [20.7, 22.77, 24.84, 26.91]
            }]
        },
        3016: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_str01_hand_02.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [46, 46, 46, 46]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.245, .245, .245, .245]
            }]
        },
        3019: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_agi01_body_01.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        3023: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_burst01_body_01.png",
            SuitId: "suit_burst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        3024: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_usp01_body_02.png",
            SuitId: "suit_usp01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.0875, .0875, .0875, .0875]
            }]
        },
        3026: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_body_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [16, 16, 16, 16]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [27, 27, 27, 27]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [18, 18, 18, 18]
            }, {
                AttrType: 1,
                Formula: "BaseFinalAddition",
                Values: [125.3763938565117, 125.3763938565117, 125.3763938565117, 125.3763938565117]
            }]
        },
        3028: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_parts_tundra01_edc_04.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.228, .228, .228, .228]
            }]
        },
        3029: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_body_03.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        3036: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_parts_tundra01_edc_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.057, .057, .057, .057]
            }]
        },
        3037: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_usp02_edc_02.png",
            SuitId: "suit_usp02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        3038: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_edc_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.8223684210526316, .8080155138978669, .7941550190597205, .7807620237351656]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.8223684210526316, .8080155138978669, .7941550190597205, .7807620237351656]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.8223684210526316, .8080155138978669, .7941550190597205, .7807620237351656]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.8223684210526316, .8080155138978669, .7941550190597205, .7807620237351656]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.8223684210526316, .8080155138978669, .7941550190597205, .7807620237351656]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.8223684210526316, .8080155138978669, .7941550190597205, .7807620237351656]
            }]
        },
        3041: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_agi01_edc_03.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        3042: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_hand_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [86, 94, 103, 111]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.24, .264, .288, .312]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.24, .264, .288, .312]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.24, .264, .288, .312]
            }]
        },
        3044: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_hand_01.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [46, 46, 46, 46]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 61,
                Formula: "BaseAddition",
                Values: [.245, .245, .245, .245]
            }]
        },
        3046: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_will01_edc_02.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        3049: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_parts_tundra01_edc_03.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.057, .057, .057, .057]
            }]
        },
        3050: {
            Rarity: 1,
            Icon: "/ui/ef/itemicon/item_equip_t0_parts_tundra01_hand_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [6, 6, 6, 6]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [11, 11, 11, 11]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [7, 7, 7, 7]
            }, {
                AttrType: 1,
                Formula: "BaseFinalAddition",
                Values: [77.21228697664634, 77.21228697664634, 77.21228697664634, 77.21228697664634]
            }]
        },
        3051: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_body_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 65, 65, 65]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 43, 43, 43]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.078, .078, .078, .078]
            }]
        },
        3052: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_usp01_edc_02.png",
            SuitId: "suit_usp01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.3675, .3675, .3675, .3675]
            }]
        },
        3053: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_hand_03.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.08625, .094875, .1035, .11212499999999999]
            }]
        },
        3056: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_agi01_edc_02.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.21, .21, .21, .21]
            }]
        },
        3057: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_will01_edc_01.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.147, .147, .147, .147]
            }]
        },
        3059: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_wisd01_hand_01.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [46, 46, 46, 46]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.1225, .1225, .1225, .1225]
            }]
        },
        3060: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_hand_01.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.345, .3795, .414, .44849999999999995]
            }]
        },
        3061: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_body_02.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }]
        },
        3064: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_edc_03.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.5175, .56925, .6209999999999999, .67275]
            }]
        },
        3065: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_body_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [65, 65, 65, 65]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 43, 43, 43]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.039, .039, .039, .039]
            }]
        },
        3066: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_body_01.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.25875, .284625, .31049999999999994, .336375]
            }]
        },
        3067: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_body_04.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        3068: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_edc_01.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [41.4, 45.54, 49.68, 53.82]
            }]
        },
        3072: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_usp02_hand_01.png",
            SuitId: "suit_usp02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.20535714285714285, .22589285714285715, .2464285714285714, .2669642857142857]
            }]
        },
        3075: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_will01_hand_01.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [46, 46, 46, 46]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.1225, .1225, .1225, .1225]
            }]
        },
        3076: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_wisd01_body_02.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        3077: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_hand_02.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        3078: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_poise01_hand_01.png",
            SuitId: "suit_poise01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [34.5, 37.95, 41.4, 44.85]
            }]
        },
        3079: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_parts_tundra01_hand_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21.599999999999998, 21.599999999999998, 21.599999999999998, 21.599999999999998]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [36, 36, 36, 36]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [24, 24, 24, 24]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.19, .19, .19, .19]
            }]
        },
        3080: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_body_05.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        3081: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_poise01_body_01.png",
            SuitId: "suit_poise01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 61,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        3082: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_poise01_hand_02.png",
            SuitId: "suit_poise01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }]
        },
        3089: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_body_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [16, 16, 16, 16]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [27, 27, 27, 27]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [18, 18, 18, 18]
            }, {
                AttrType: 1,
                Formula: "BaseFinalAddition",
                Values: [125.3763938565117, 125.3763938565117, 125.3763938565117, 125.3763938565117]
            }]
        },
        3092: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_usp02_hand_01.png",
            SuitId: "suit_usp02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.20535714285714285, .22589285714285715, .2464285714285714, .2669642857142857]
            }]
        },
        3093: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_edc_05.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3095: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_edc_04.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 10001,
                Formula: "BaseMultiplier",
                Values: [.2070178350109774, .22771961851207514, .24842140201317287, .2691231855142706]
            }]
        },
        3096: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_poise01_edc_02.png",
            SuitId: "suit_poise01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [41.4, 45.54, 49.68, 53.82]
            }]
        },
        3097: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_pulse_cryst01_body_01.png",
            SuitId: "suit_pulse_cryst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [20.7, 22.77, 24.84, 26.91]
            }]
        },
        3099: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_wisd01_edc_01.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        3100: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_edc_04.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.175, .175, .175, .175]
            }]
        },
        3101: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atk02_edc_02.png",
            SuitId: "suit_atk02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.5175, .56925, .6209999999999999, .67275]
            }]
        },
        3104: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_wisd01_body_01.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 17,
                Formula: "BaseAddition",
                Values: [.09799999999999999, .09799999999999999, .09799999999999999, .09799999999999999]
            }]
        },
        3105: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_body_02.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.207, .2277, .24839999999999998, .2691]
            }]
        },
        3106: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_str01_hand_01.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21.599999999999998, 21.599999999999998, 21.599999999999998, 21.599999999999998]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [33, 33, 33, 33]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [22, 22, 22, 22]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.9195402298850576, .9195402298850576, .9195402298850576, .9195402298850576]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.9195402298850576, .9195402298850576, .9195402298850576, .9195402298850576]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.9195402298850576, .9195402298850576, .9195402298850576, .9195402298850576]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.9195402298850576, .9195402298850576, .9195402298850576, .9195402298850576]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.9195402298850576, .9195402298850576, .9195402298850576, .9195402298850576]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.9195402298850576, .9195402298850576, .9195402298850576, .9195402298850576]
            }]
        },
        3107: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_parts_tundra01_hand_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21.599999999999998, 21.599999999999998, 21.599999999999998, 21.599999999999998]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [36, 36, 36, 36]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [24, 24, 24, 24]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.095, .095, .095, .095]
            }]
        },
        3108: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_wisd01_edc_02.png",
            SuitId: "suit_wisd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [29, 29, 29, 29]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.175, .175, .175, .175]
            }]
        },
        3109: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_body_02.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 17,
                Formula: "BaseAddition",
                Values: [.13799999999999998, .1518, .16559999999999997, .17939999999999998]
            }]
        },
        3114: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_edc_03.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.2571428571428571, .28285714285714286, .30857142857142855, .33428571428571424]
            }]
        },
        3116: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_edc_02.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [41, 45, 49, 53]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3119: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_str01_edc_01.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.105, .105, .105, .105]
            }]
        },
        3121: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_agi01_hand_01.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [46, 46, 46, 46]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.1225, .1225, .1225, .1225]
            }]
        },
        3122: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_edc_06.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3123: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_edc_02.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3124: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_fire_natr01_hand_02.png",
            SuitId: "suit_fire_natr01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        3126: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_usp02_edc_03.png",
            SuitId: "suit_usp02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.2464285714285714, .2710714285714286, .2957142857142857, .32035714285714284]
            }]
        },
        3129: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_body_01.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        3130: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_poise01_edc_03.png",
            SuitId: "suit_poise01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        3133: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_usp01_body_01.png",
            SuitId: "suit_usp01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.18375, .18375, .18375, .18375]
            }]
        },
        3138: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_suit_stragi01_hand_01.png",
            SuitId: "suit_stragi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [16.8, 16.8, 16.8, 16.8]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 4,
                Formula: "BaseFinalMultiplier",
                Values: [.936768149882904, .936768149882904, .936768149882904, .936768149882904]
            }, {
                AttrType: 5,
                Formula: "BaseFinalMultiplier",
                Values: [.936768149882904, .936768149882904, .936768149882904, .936768149882904]
            }, {
                AttrType: 6,
                Formula: "BaseFinalMultiplier",
                Values: [.936768149882904, .936768149882904, .936768149882904, .936768149882904]
            }, {
                AttrType: 7,
                Formula: "BaseFinalMultiplier",
                Values: [.936768149882904, .936768149882904, .936768149882904, .936768149882904]
            }, {
                AttrType: 48,
                Formula: "BaseFinalMultiplier",
                Values: [.936768149882904, .936768149882904, .936768149882904, .936768149882904]
            }, {
                AttrType: 60,
                Formula: "BaseFinalMultiplier",
                Values: [.936768149882904, .936768149882904, .936768149882904, .936768149882904]
            }]
        },
        3139: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_edc_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.43199999999999994, .47519999999999996, .5183999999999999, .5616]
            }]
        },
        3142: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_body_06.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [22.400000000000002, 22.400000000000002, 22.400000000000002, 22.400000000000002]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [37, 37, 37, 37]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [25, 25, 25, 25]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.09, .09, .09, .09]
            }]
        },
        3143: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_parts_wuling01_body_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [115, 126, 138, 149]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.12857142857142856, .14142857142857143, .15428571428571428, .16714285714285712]
            }]
        },
        3145: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_usp02_edc_01.png",
            SuitId: "suit_usp02",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.2464285714285714, .2710714285714286, .2957142857142857, .32035714285714284]
            }]
        },
        3148: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_str01_body_01.png",
            SuitId: "suit_str01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.147, .147, .147, .147]
            }]
        },
        3150: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_agi01_edc_01.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.105, .105, .105, .105]
            }]
        },
        3151: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_edc_02.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        3155: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_body_01.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.1035, .11385, .12419999999999999, .13455]
            }]
        },
        3164: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_will01_edc_01.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.105, .105, .105, .105]
            }]
        },
        3166: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_burst01_edc_01.png",
            SuitId: "suit_burst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        3167: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_edc_01.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        3170: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_edc_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [6, 6, 6, 6]
            }, {
                AttrType: 2,
                Formula: "BaseMultiplier",
                Values: [.132, .132, .132, .132]
            }]
        },
        3171: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_body_02.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 10001,
                Formula: "BaseMultiplier",
                Values: [.1035089175054887, .11385980925603757, .12421070100658643, .1345615927571353]
            }]
        },
        3172: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_body_05.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [22.400000000000002, 22.400000000000002, 22.400000000000002, 22.400000000000002]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [37, 37, 37, 37]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [25, 25, 25, 25]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.09, .09, .09, .09]
            }]
        },
        3176: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_usp01_hand_01.png",
            SuitId: "suit_usp01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [46, 46, 46, 46]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [30, 30, 30, 30]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [24.5, 24.5, 24.5, 24.5]
            }]
        },
        3178: {
            Rarity: 2,
            Icon: "/ui/ef/itemicon/item_equip_t1_parts_tundra01_hand_01.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [12, 12, 12, 12]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [20, 20, 20, 20]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [13, 13, 13, 13]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.11, .11, .11, .11]
            }]
        },
        3179: {
            Rarity: 3,
            Icon: "/ui/ef/itemicon/item_equip_t2_suit_will01_edc_02.png",
            SuitId: "suit_will01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [10.799999999999999, 10.799999999999999, 10.799999999999999, 10.799999999999999]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.105, .105, .105, .105]
            }]
        },
        3180: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_agi01_edc_02.png",
            SuitId: "suit_agi01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [23, 23, 23, 23]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.3675, .3675, .3675, .3675]
            }]
        },
        3181: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_hand_01.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.20535714285714285, .22589285714285715, .2464285714285714, .2669642857142857]
            }]
        },
        3182: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_edc_04.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [31, 31, 31, 31]
            }, {
                AttrType: 29,
                Formula: "BaseAddition",
                Values: [.156, .156, .156, .156]
            }]
        },
        3183: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_parts_tundra01_edc_02.png",
            SuitId: "",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [15, 15, 15, 15]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [31, 31, 31, 31]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.312, .312, .312, .312]
            }]
        },
        3185: {
            Rarity: 4,
            Icon: "/ui/ef/itemicon/item_equip_t3_suit_atk01_body_01.png",
            SuitId: "suit_atk01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [40, 40, 40, 40]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [61, 61, 61, 61]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [41, 41, 41, 41]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.09799999999999999, .09799999999999999, .09799999999999999, .09799999999999999]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.09799999999999999, .09799999999999999, .09799999999999999, .09799999999999999]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.09799999999999999, .09799999999999999, .09799999999999999, .09799999999999999]
            }]
        },
        3187: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_pulse_cryst01_edc_01.png",
            SuitId: "suit_pulse_cryst01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [41.4, 45.54, 49.68, 53.82]
            }]
        },
        3190: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_edc_06.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3191: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_edc_05.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.1035, .11385, .12419999999999999, .13455]
            }]
        },
        3243: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_heal01_edc_01.png",
            SuitId: "suit_heal01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 1,
                Formula: "BaseMultiplier",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3250: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_hand_04.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.43125, .47437500000000005, .5175, .560625]
            }]
        },
        3252: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_edc_07.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        3255: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_edc_06.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 9,
                Formula: "BaseAddition",
                Values: [.1035, .11385, .12419999999999999, .13455]
            }]
        },
        3258: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_criti01_body_06.png",
            SuitId: "suit_criti01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        3259: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_body_05.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }]
        },
        4107: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_hand_03.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.20535714285714285, .22589285714285715, .2464285714285714, .2669642857142857]
            }]
        },
        4125: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_edc_02.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        4127: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_atb01_edc_06.png",
            SuitId: "suit_atb01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 10001,
                Formula: "BaseMultiplier",
                Values: [.2070178350109774, .22771961851207514, .24842140201317287, .2691231855142706]
            }]
        },
        4133: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_edc_04.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.5175, .56925, .6209999999999999, .67275]
            }]
        },
        4135: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_attri01_hand_03.png",
            SuitId: "suit_attri01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        4138: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_body_03.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 50,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }]
        },
        4139: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_phy01_hand_03.png",
            SuitId: "suit_phy01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [34.5, 37.95, 41.4, 44.85]
            }]
        },
        4161: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_expend_spell01_edc_02.png",
            SuitId: "suit_expend_spell01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        4163: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_combo_cd01_body_01.png",
            SuitId: "suit_combo_cd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.1232142857142857, .1355357142857143, .14785714285714285, .16017857142857142]
            }]
        },
        4165: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_combo_cd01_hand_01.png",
            SuitId: "suit_combo_cd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }, {
                AttrType: 28,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }, {
                AttrType: 33,
                Formula: "BaseAddition",
                Values: [.23, .25300000000000006, .276, .29900000000000004]
            }]
        },
        4166: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_combo_cd01_body_02.png",
            SuitId: "suit_combo_cd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [20.7, 22.77, 24.84, 26.91]
            }]
        },
        4169: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_combo_cd01_edc_02.png",
            SuitId: "suit_combo_cd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 51,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }, {
                AttrType: 54,
                Formula: "BaseAddition",
                Values: [.22999999999999998, .253, .27599999999999997, .299]
            }]
        },
        4172: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_expend_spell01_hand_02.png",
            SuitId: "suit_expend_spell01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.19166666666666668, .21083333333333337, .23, .2491666666666667]
            }]
        },
        4174: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_combo_cd01_edc_01.png",
            SuitId: "suit_combo_cd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 40,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 39,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 32,
                Formula: "BaseAddition",
                Values: [.414, .4554, .49679999999999996, .5382]
            }]
        },
        4178: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_expend_spell01_body_02.png",
            SuitId: "suit_expend_spell01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [56, 56, 56, 56]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [87, 95, 104, 113]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [58, 63, 69, 75]
            }, {
                AttrType: 53,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }, {
                AttrType: 52,
                Formula: "BaseAddition",
                Values: [.11499999999999999, .1265, .13799999999999998, .1495]
            }]
        },
        4181: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_combo_cd01_hand_02.png",
            SuitId: "suit_combo_cd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [42, 42, 42, 42]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [65, 71, 78, 84]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [43, 47, 51, 55]
            }, {
                AttrType: 44,
                Formula: "BaseAddition",
                Values: [.20535714285714285, .22589285714285715, .2464285714285714, .2669642857142857]
            }]
        },
        4199: {
            Rarity: 5,
            Icon: "/ui/ef/itemicon/item_equip_t4_suit_combo_cd01_edc_03.png",
            SuitId: "suit_combo_cd01",
            AttrModifiers: [{
                AttrType: 3,
                Formula: "BaseAddition",
                Values: [21, 21, 21, 21]
            }, {
                AttrType: 41,
                Formula: "BaseAddition",
                Values: [32, 35, 38, 41]
            }, {
                AttrType: 42,
                Formula: "BaseAddition",
                Values: [21, 23, 25, 27]
            }, {
                AttrType: 87,
                Formula: "BaseAddition",
                Values: [41.4, 45.54, 49.68, 53.82]
            }]
        }
    },
    Suits: {
        suit_agi01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_agi01.png",
            NameHash: "-554118021033979760",
            SkillId: 1082
        },
        suit_atb01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_atb01.png",
            NameHash: "-6465152567770222340",
            SkillId: 1067
        },
        suit_atk01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_atk01.png",
            NameHash: "2134558188647797356",
            SkillId: 2071
        },
        suit_atk02: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_atk02.png",
            NameHash: "-7630189515413167967",
            SkillId: 2072
        },
        suit_attri01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_attri01.png",
            NameHash: "-5935672926878943329",
            SkillId: 1066
        },
        suit_burst01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_burst01.png",
            NameHash: "8727527172877146838",
            SkillId: 2073
        },
        suit_combo_cd01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_attri01.png",
            NameHash: "-4308353162611329431",
            SkillId: 2846
        },
        suit_criti01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_criti01.png",
            NameHash: "1298184612084436356",
            SkillId: 1068
        },
        suit_expend_spell01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_usp02.png",
            NameHash: "-2034262180626135930",
            SkillId: 2847
        },
        suit_fire_natr01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_fire_natr01.png",
            NameHash: "-6815447793938838187",
            SkillId: 1040
        },
        suit_heal01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_heal01.png",
            NameHash: "-5627439031669466608",
            SkillId: 1041
        },
        suit_phy01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_phy01.png",
            NameHash: "2969356566561953360",
            SkillId: 1069
        },
        suit_poise01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_poise01.png",
            NameHash: "4652490134760473367",
            SkillId: 1042
        },
        suit_pulse_cryst01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_pulse_cryst01.png",
            NameHash: "-8956651590176334632",
            SkillId: 1039
        },
        suit_str01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_str01.png",
            NameHash: "-8144875526851308493",
            SkillId: 1083
        },
        suit_stragi01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_stragi01.png",
            NameHash: "8944173534973994402",
            SkillId: 1911
        },
        suit_usp01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_usp01.png",
            NameHash: "-1756686334412141542",
            SkillId: 2074
        },
        suit_usp02: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_wuling_suit_usp02.png",
            NameHash: "-3082031696843561092",
            SkillId: 2075
        },
        suit_will01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_will01.png",
            NameHash: "-921493216370650704",
            SkillId: 1084
        },
        suit_wisd01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_wisd01.png",
            NameHash: "-5097897904282876005",
            SkillId: 1085
        },
        suit_wisdwill01: {
            Icon: "/ui/ef/equipmentlogobigwhite/icon_pack_tundra_suit_wisdwill01.png",
            NameHash: "7450612431920625701",
            SkillId: 1912
        }
    }
}
  , M0 = {
    3: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0004_pelica.png"
    },
    4: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0011_seraph.png"
    },
    5: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0021_whiten.png"
    },
    6: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0023_antal.png"
    },
    7: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0026_lastrite.png"
    },
    8: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0015_lifeng.png"
    },
    9: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0022_bounda.png"
    },
    10: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0006_wolfgd.png"
    },
    11: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0009_azrila.png"
    },
    12: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0012_avywen.png"
    },
    13: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0013_aglina.png"
    },
    14: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0014_aurora.png"
    },
    15: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0003_endminf.png"
    },
    16: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0005_chen.png"
    },
    17: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0024_deepfin.png"
    },
    18: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0019_karin.png"
    },
    19: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0020_meurs.png"
    },
    20: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0025_ardelia.png"
    },
    21: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0002_endminm.png"
    },
    22: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0007_ikut.png"
    },
    23: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0016_laevat.png"
    },
    24: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0017_yvonne.png"
    },
    25: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0018_dapan.png"
    },
    26: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0029_pograni.png"
    },
    27: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_bp_1.png"
    },
    28: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_bp_1_1.png"
    },
    29: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0027_tangtang.png"
    },
    30: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0028_wulfa.png"
    },
    31: {
        Icon: "/ui/ef/charremoteicon/icon_chr_0030_zhuangfy.png"
    },
    32: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_activity_1.png"
    },
    33: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_bp_1_2.png"
    },
    34: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_activity_2.png"
    },
    35: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_activity_3.png"
    },
    36: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_activity_4.png"
    },
    38: {
        Icon: "/ui/ef/playeravatar/icon_user_avatar_activity_6.png"
    }
}
  , L0 = {
    3: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_normal_1.png"
    },
    4: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_normal_2.png"
    },
    5: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_normal_3.png"
    },
    6: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0009_azrila.png"
    },
    7: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0029_pograni.png"
    },
    8: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0013_aglina.png"
    },
    9: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0015_lifeng.png"
    },
    10: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0016_laevat.png"
    },
    11: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0026_lastrite.png"
    },
    12: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0017_yvonne.png"
    },
    13: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0025_ardelia.png"
    },
    14: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_bp_1.png"
    },
    15: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_bp_1_1.png"
    },
    16: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0028_wulfa.png"
    },
    17: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0027_tangtang.png"
    },
    18: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_chr_0030_zhuangfy.png"
    },
    19: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_bp_1_2.png"
    },
    20: {
        Icon: "/ui/ef/friendlistbg/business_card_topic_normal_4.png"
    }
}
  , w0 = {
    4: "0.11553491844115361,-0.06161103925233647,0.7503645600000003,0",
    6: "-0.02949228059236181,-0.37195626168224316,0.990264,0",
    8: "0.12444634970122119,-0.3213831775700934,0.7773333333333333,0",
    10: "0.12332462977396726,-0.3597009345794392,0.759,0",
    11: "0.1411374642764354,-0.366803738317757,0.7355333333333335,0",
    12: "0.09988812899454379,-0.25821095327102817,0.8265510000000004,0",
    13: "0.06049818442712393,-0.38057325981308454,0.8035513200000002,0",
    14: "0.05407200567186237,-0.20471231850467314,0.8878595220000004,0",
    20: "0.09687509518316423,-0.5427418242990657,0.7660171200000002,0",
    22: "0.2529941462490792,-0.3025824875532216,0.524967911553933,0",
    23: "0.17449742447388925,-0.30115581308411243,0.7315175999999999,0",
    24: "0.16282236632891653,-0.1955207476635514,0.7376159999999999,0",
    26: "0.13546396466614696,-0.4432523364485982,0.7509333333333335,0",
    27: "0.15845006495193545,-0.4054953271028037,0.6812666666666668,0",
    28: "0.26848786195920593,-0.29439349695258227,0.5145210501140097,0",
    30: "0.10490925472180834,-0.240079248346535,0.6471804286252805,0",
    31: "0.17453902831904372,-0.3141383177570095,0.5937066666666669,0",
    32: "0.19784344505066243,-0.09417943925233664,0.6032400000000001,0",
    33: "0.17350166484801235,-0.16002915887850486,0.5488560000000002,0",
    35: "0.3301993244998701,-0.18755140186915895,0.4370666666666666,0",
    40: "0.13217199272538313,-0.15682242990654202,0.7533333333333334,0",
    42: "0.16510774227071962,-0.39390654205607467,0.7120666666666668,0",
    43: "0.11288007092751352,-0.23201383177570084,0.8072459999999998,0",
    44: "0.11225178659392034,-0.27553072897196274,0.7435692000000002,0"
};

var _1 = (a, e, i) => {
    if (!e.has(a))
        throw TypeError("Cannot " + i)
}
, J = (a, e, i) => (_1(a, e, "read from private field"),
i ? i.call(a) : e.get(a)), x0 = (a, e, i) => {
    if (e.has(a))
        throw TypeError("Cannot add the same private member more than once");
    e instanceof WeakSet ? e.add(a) : e.set(a, i)
}
, G0 = (a, e, i, t) => (_1(a, e, "write to private field"),
t ? t.call(a, i) : e.set(a, i),
i), f;
const Ie = O0
  , F0 = N0
  , Z = V0
  , Ki = A("Element", {
    Cryst: "Cryst",
    Fire: "Fire",
    Pulse: "Pulse",
    Natural: "Natural",
    Physical: "Physical"
});
A("Role", {
    SUPPORTER: "SUPPORTER",
    DEFENDER: "DEFENDER",
    VANGUARD: "VANGUARD",
    ASSAULT: "ASSAULT",
    GUARD: "GUARD",
    CASTER: "CASTER"
});
const ji = A("WeaponType", {
    Sword: "Sword",
    Wand: "Wand",
    Claymores: "Claymores",
    Lance: "Lance",
    Pistol: "Pistol"
})
  , Xi = A("NodeSkillType", {
    CharBreak: 1,
    EquipBreak: 2,
    Attribute: 3,
    Passive: 4,
    Factory: 5
});
A("WeaponType", {
    GEN_MALE: 1,
    GEN_FEMALE: 2
});
const y = A("Prop", {
    Main_base: -1e4,
    Main_ratio: 1e4,
    Main_delta: -1e5,
    Sub_base: -10001,
    Sub_ratio: 10001,
    Sub_delta: -100001,
    Level: 0,
    MaxHp_base: 1,
    MaxHp_ratio: -1001,
    MaxHp_delta: -1,
    Atk_base: 2,
    Atk_ratio: -2001,
    Atk_delta: -2,
    Atk_total_ratio: -2002,
    Def_base: 3,
    Def_ratio: -3001,
    Def_delta: -3,
    PhysicalDamageTakenScalar_base: 4,
    PhysicalDamageTakenScalar_delta: -4,
    FireDamageTakenScalar_base: 5,
    FireDamageTakenScalar_delta: -5,
    PulseDamageTakenScalar_base: 6,
    PulseDamageTakenScalar_delta: -6,
    CrystDamageTakenScalar_base: 7,
    CrystDamageTakenScalar_delta: -7,
    Weight: 8,
    CriticalRate_base: 9,
    CriticalRate_delta: -9,
    CriticalDamageIncrease_base: 10,
    CriticalDamageIncrease_delta: -10,
    Hatred: 11,
    NormalAttackRange: 12,
    MoveSpeedScalar: 13,
    TurnRateScalar: 14,
    AttackRate: 15,
    SkillCooldownScalar: 16,
    NormalAttackDamageIncrease_base: 17,
    NormalAttackDamageIncrease_delta: -17,
    HpRecoveryPerSec: 18,
    HpRecoveryPerSecByMaxHpRatio: 19,
    MaxPoise: 20,
    PoiseRecTime: 21,
    MaxUltimateSp: 22,
    DamageTakenScalarWithPoise: 23,
    PoiseDamageTakenScalar: 24,
    PhysicalInflictionDamageScalar: 25,
    PoiseDamageOutputScalar_base: 26,
    PoiseDamageOutputScalar_delta: -26,
    BreakingAttackDamageTakenScalar: 27,
    UltimateSkillDamageIncrease_base: 28,
    UltimateSkillDamageIncrease_delta: -28,
    HealOutputIncrease_base: 29,
    HealOutputIncrease_delta: -29,
    HealTakenIncrease_base: 30,
    HealTakenIncrease_delta: -30,
    PoiseRecTimeScalar: 31,
    NormalSkillDamageIncrease_base: 32,
    NormalSkillDamageIncrease_delta: -32,
    ComboSkillDamageIncrease_base: 33,
    ComboSkillDamageIncrease_delta: -33,
    KnockDownTimeAddition: 34,
    FireBurstDamageIncrease_base: 35,
    FireBurstDamageIncrease_delta: -35,
    PulseBurstDamageIncrease_base: 36,
    PulseBurstDamageIncrease_delta: -36,
    CrystBurstDamageIncrease_base: 37,
    CrystBurstDamageIncrease_delta: -37,
    NaturalBurstDamageIncrease_base: 38,
    NaturalBurstDamageIncrease_delta: -38,
    Str_base: 39,
    Str_ratio: -39001,
    Str_delta: -39,
    Agi_base: 40,
    Agi_ratio: -40001,
    Agi_delta: -40,
    Wisd_base: 41,
    Wisd_ratio: -41001,
    Wisd_delta: -41,
    Will_base: 42,
    Will_ratio: -42001,
    Will_delta: -42,
    LifeSteal: 43,
    UltimateSpGainScalar_base: 44,
    UltimateSpGainScalar_delta: -44,
    AtbCostAddition: 45,
    SkillCooldownAddition: 46,
    ComboSkillCooldownScalar_base: 47,
    ComboSkillCooldownScalar_delta: -47,
    NaturalDamageTakenScalar_base: 48,
    NaturalDamageTakenScalar_delta: -48,
    IgniteDamageScalar: 49,
    PhysicalDamageIncrease_base: 50,
    PhysicalDamageIncrease_delta: -50,
    FireDamageIncrease_base: 51,
    FireDamageIncrease_delta: -51,
    PulseDamageIncrease_base: 52,
    PulseDamageIncrease_delta: -52,
    CrystDamageIncrease_base: 53,
    CrystDamageIncrease_delta: -53,
    NaturalDamageIncrease_base: 54,
    NaturalDamageIncrease_delta: -54,
    EtherDamageIncrease_base: 55,
    EtherDamageIncrease_delta: -55,
    ArtsDamageIncrease: -100,
    AllSkillDamageIncrease: -101,
    FireAbnormalDamageIncrease_base: 56,
    FireAbnormalDamageIncrease_delta: -56,
    PulseAbnormalDamageIncrease_base: 57,
    PulseAbnormalDamageIncrease_delta: -57,
    CrystAbnormalDamageIncrease_base: 58,
    CrystAbnormalDamageIncrease_delta: -58,
    NaturalAbnormalDamageIncrease_base: 59,
    NaturalAbnormalDamageIncrease_delta: -59,
    EtherDamageTakenScalar_base: 60,
    EtherDamageTakenScalar_delta: -60,
    DamageToBrokenUnitIncrease_base: 61,
    DamageToBrokenUnitIncrease_delta: -61,
    WeaknessDmgScalar: 62,
    ShelterDmgScalar: 63,
    PhysicalEnhancedDmgIncrease: 64,
    FireEnhancedDmgIncrease: 65,
    PulseEnhancedDmgIncrease: 66,
    CrystEnhancedDmgIncrease: 67,
    NaturalEnhancedDmgIncrease: 68,
    EtherEnhancedDmgIncrease: 69,
    PhysicalVulnerableDmgIncrease: 70,
    FireVulnerableDmgIncrease: 71,
    PulseVulnerableDmgIncrease: 72,
    CrystVulnerableDmgIncrease: 73,
    NaturalVulnerableDmgIncrease: 74,
    EtherVulnerableDmgIncrease: 75,
    AtkIncreaseFactorFromStr: 76,
    AtkIncreaseFactorFromAgi: 77,
    AtkIncreaseFactorFromWisd: 78,
    AtkIncreaseFactorFromWill: 79,
    PhysicalDmgResistScalar_base: 80,
    PhysicalDmgResistScalar_delta: -80,
    NaturalDmgResistScalar_base: 81,
    NaturalDmgResistScalar_delta: -81,
    CrystDmgResistScalar_base: 82,
    CrystDmgResistScalar_delta: -82,
    PulseDmgResistScalar_base: 83,
    PulseDmgResistScalar_delta: -83,
    FireDmgResistScalar_base: 84,
    FireDmgResistScalar_delta: -84,
    EtherDmgResistScalar_base: 85,
    EtherDmgResistScalar_delta: -85,
    SlowActionSpeedScalar: 86,
    PhysicalAndSpellInflictionEnhance_base: 87,
    PhysicalAndSpellInflictionEnhance_delta: -87,
    ShieldOutputIncrease: 88,
    ShieldTakenIncrease: 89,
    NormalAttackStartRange: 90
});
A("EquipType", {
    BODY: 0,
    HAND: 1,
    EDC1: 2,
    EDC2: 3
});
const z0 = {
    charBreak20: 1,
    equipBreakT2: 1,
    charBreak40: 2,
    equipBreakT3: 2,
    charBreak60: 3,
    equipBreakT4: 3,
    charBreak70: 4
}
  , b0 = ae[g.EF];
var V;
class W0 {
    constructor(e) {
        R(this, V, void 0);
        this.weapon = null,
        this.relics = new Array(4).fill(null),
        u(this, V, null),
        this.data = e,
        this.meta = J0[e.templateId],
        e.weapon && (this.weapon = new d1(e.weapon));
        for (let i of e.equip) {
            const t = i.value;
            let n = i.key;
            n == 1 ? n = 0 : n == 0 && (n = 1);
            const o = new S1(t);
            this.relics[n] = o
        }
    }
    get level() {
        return this.data.level || 1
    }
    get ascension() {
        return z0[this.data.talent.latestBreakNode] || 0
    }
    get const() {
        return this.data.potentialLevel || 0
    }
    get skills() {
        const e = {};
        for (const c of this.data.skillInfo.levelInfo)
            e[c.skillId] = c.skillLevel;
        const i = new Map([["dispNormalAttackSkill", 0], ["normalSkill", 1], ["comboSkill", 2], ["ultimateSkill", 3]]);
        let t = new Array(4).fill(null);
        for (var n of i.keys()) {
            var o = e[this.data.skillInfo[n]]
              , p = this.data.skillInfo[n];
            t[i.get(n)] = {
                id: p,
                level: o
            }
        }
        return t
    }
    get smallImage() {
        return `/ui/ef/charroundicon/icon_round_${this.data.variantId || this.meta.excel.StrId}.png`
    }
    get splashImage() {
        return `/ui/ef/splash/${this.data.variantId || this.meta.excel.StrId}.webp`
    }
    get tileImage() {
        return this.smallImage
    }
    get flavorImage() {
        return `/ui/ef/charinfo/bg_charinfo_${this.data.variantId || this.meta.excel.StrId}.png`
    }
    get splashImageOffset() {
        return w0[this.meta.id] || ""
    }
    relicSets(e=this.relics) {
        const i = new Map;
        for (const t of e) {
            if (!t)
                continue;
            const n = t.meta.set.Id;
            if (!n)
                continue;
            let o = i.get(n) || new Q0(n);
            i.set(n, o),
            o.count++,
            o.relics.push(t)
        }
        for (let[t,n] of i) {
            if (n.count < 3) {
                i.delete(t);
                continue
            }
            if (n.count >= 3) {
                n.count = 3;
                continue
            }
        }
        return [...i.values()]
    }
    get hash() {
        if (s(this, V))
            return s(this, V);
        let e = "";
        return e += "" + this.meta.id + this.ascension + this.level + this.const + this.data.skillInfo.levelInfo.map(i => String(i.skillLevel)).join("") + this.data.talent.attrNodes.map(i => i.split("_").at(-1)).join("") + this.data.talent.latestPassiveSkillNodes.map(i => i.split("_").slice(-2).join("")).join("") + this.data.talent.latestFactorySkillNodes.map(i => i.split("_").slice(-2).join("")).join(""),
        u(this, V, e),
        e
    }
}
V = new WeakMap;
class l1 {
    constructor(e) {
        this.id = e;
        const i = u1;
        this.excel = i[e]
    }
    get nameHash() {
        return this.excel.NameHash
    }
    get element() {
        return this.excel.Element
    }
    get role() {
        return this.excel.Profession
    }
    get rarity() {
        return this.excel.Rarity
    }
    get elementColor() {
        return ei[this.element]
    }
    get rarityColor() {
        return ii[this.rarity]
    }
}
const Y0 = {
    BaseAddition: "_base",
    BaseMultiplier: "_ratio",
    BaseFinalMultiplier: "_delta",
    BaseFinalAddition: "_delta",
    Addition: "_delta"
}
  , oe = class S {
    constructor(e, i, t=null) {
        x0(this, f, 0),
        this.id = e,
        this.value = i,
        this.level = t,
        G0(this, f, S.typeFromName(this.name))
    }
    get type() {
        return J(this, f)
    }
    static typeFromName(e) {
        return e.includes("_ratio") || e.includes("Increase") || e.includes("Gain") || e.includes("Rate") || e.includes("Effi") || e.includes("Cooldown") || e.includes("Poise") ? 1 : e.includes("DamageTakenScalar") ? 3 : 0
    }
    get formatted() {
        if (J(this, f) === 0) {
            const e = String(Math.floor(this.value)).split("");
            return e.length > 3 && e.splice(e.length - 3, 0, ","),
            e.join("")
        }
        if (J(this, f) === 1)
            return ((this.value + 1e-4) * 100).toFixed(1) + "%";
        if (J(this, f) === 3)
            return ((1 - this.value) * 100).toFixed(1) + "%"
    }
    get name() {
        return y.hasOwnProperty(this.id) ? y[this.id] : (console.error("PROP NOT FOUND:", this.id, this.value, this.level),
        "")
    }
    get simpleName() {
        return this.name.replace(/_base|_ratio|_delta/g, "")
    }
    subtract(e) {
        return new g1.Property(this.id,this.value - e.value,this.level)
    }
    get icon() {
        return "/ui/ef/attributeicon/" + this.simpleName + ".png"
    }
    remake(e) {
        if (!e)
            return this;
        const i = Y0[e];
        i || console.error("Formula format not found:", e);
        const t = this.simpleName + i
          , n = y[t];
        return n || console.error("Prop name not found, tried to look up:", t),
        new S(n,this.value)
    }
    convert(e) {
        const i = e.meta.excel.MainAttrId
          , t = e.meta.excel.SubAttrId;
        switch (this.id) {
        case y.Main_base:
            return new S(i,this.value).remake("Addition").id;
        case y.Main_ratio:
            return new S(i,this.value).remake("BaseMultiplier").id;
        case y.Main_delta:
            return new S(i,this.value).remake("Addition").id;
        case y.Sub_base:
            return new S(t,this.value).remake("Addition").id;
        case y.Sub_ratio:
            return new S(t,this.value).remake("BaseMultiplier").id;
        case y.Sub_delta:
            return new S(t,this.value).remake("Addition").id;
        default:
            return this.id
        }
    }
    get isArts() {
        return S.arts.has(this.simpleName)
    }
    get isElement() {
        return S.elements.has(this.simpleName)
    }
    get isSkill() {
        return S.skills.has(this.simpleName)
    }
    static joinElements(e) {
        function i(t, n, o) {
            const p = []
              , c = [];
            for (const _ of t)
                n.includes(_.simpleName) ? c.push(_) : p.push(_);
            return c.length === n.length && new Set(c.map(_ => _.value)).size === 1 ? (p.push(new S(o,c[0].value)),
            p) : t
        }
        return e = i(e, [...S.arts.values()], y.ArtsDamageIncrease),
        e = i(e, [...S.skills.values()], y.AllSkillDamageIncrease),
        e
    }
    static mouseleave(e, i) {
        e.set([])
    }
    static mouseenter(e, i) {
        if (i.isArts) {
            e.set([i.simpleName, "ArtsDamageIncrease"]);
            return
        }
        if (i.id == y.ArtsDamageIncrease) {
            e.set([...S.arts, "ArtsDamageIncrease"]);
            return
        }
        e.set([i.simpleName])
    }
}
;
f = new WeakMap;
oe.elements = new Set(["PhysicalDamageIncrease", "FireDamageIncrease", "PulseDamageIncrease", "CrystDamageIncrease", "NaturalDamageIncrease"]);
oe.arts = new Set(["FireDamageIncrease", "PulseDamageIncrease", "CrystDamageIncrease", "NaturalDamageIncrease"]);
oe.skills = new Set(["UltimateSkillDamageIncrease", "ComboSkillDamageIncrease", "NormalSkillDamageIncrease"]);
let ie = oe;
var M;
class d1 {
    constructor(e) {
        R(this, M, void 0);
        u(this, M, null),
        this.data = e,
        this.meta = $0[e.templateId]
    }
    get level() {
        return this.data.weaponLv || 0
    }
    get ascension() {
        return this.data.breakthroughLv || 0
    }
    get refine() {
        return this.data.refineLv || 0
    }
    stats() {
        var P;
        const e = this.meta.excel.LevelTemplateId
          , i = Ie.LevelCurves[e][this.level - 1]
          , t = this.meta.excel.TalentTemplateId
          , n = this.meta.excel.BreakthroughTemplateId
          , o = Ie.TalentSkillLevelBounds[t][this.refine] || [{
            lowerBound: 0,
            upperBound: 0
        }, {
            lowerBound: 0,
            upperBound: 0
        }, {
            lowerBound: 0,
            upperBound: 0
        }]
          , p = Ie.BreakSkillLevelBounds[n][this.ascension]
          , c = [];
        for (let d in o) {
            const m = {
                lowerBound: o[d].lowerBound + p[d].lowerBound,
                upperBound: o[d].upperBound + p[d].upperBound
            };
            c.push(m)
        }
        let B = new Map;
        for (let d of ((P = this.data.attachedGem) == null ? void 0 : P.terms) || []) {
            const m = Z.TermNums[d.termNumId].TagId;
            B.set(m, d.cost)
        }
        let _ = [];
        for (let d in this.meta.excel.SkillList) {
            const m = this.meta.excel.SkillList[d]
              , Q = F0[m];
            let K = [];
            const ce = B.get(Q.TagId) || 0;
            let re = Math.min(c[d].lowerBound + ce, c[d].upperBound);
            for (let k1 in Q.PropMap) {
                const j = Number(k1)
                  , m1 = Q.PropMap[j].Values[re - 1]
                  , f1 = new ie(j,m1);
                j != y.EtherDamageIncrease_base && K.push({
                    formula: Q.PropMap[j].Formula,
                    prop: f1,
                    lower: c[d].lowerBound,
                    upper: c[d].upperBound,
                    total: re,
                    extra: ce
                })
            }
            K.length || K.push({
                lower: c[d].lowerBound,
                upper: c[d].upperBound,
                total: re,
                extra: ce
            }),
            _.push(K)
        }
        return {
            baseAtk: new ie(y.Atk_base,i),
            skillStats: _
        }
    }
    get hash() {
        var i, t, n;
        if (s(this, M))
            return s(this, M);
        const e = "" + this.meta.id + this.level + this.ascension + this.refine + (((i = this.data.attachedGem) == null ? void 0 : i.templateId) || "") + (((t = this.data.attachedGem) == null ? void 0 : t.totalCost) || "") + (((n = this.data.attachedGem) == null ? void 0 : n.terms.map(o => "" + o.termNumId + o.cost).join("")) || "");
        return u(this, M, e),
        e
    }
}
M = new WeakMap;
class A1 {
    constructor(e) {
        this.id = e;
        const i = s1;
        this.excel = i[e]
    }
    get image() {
        return this.excel.Icon.replace("ef/", "ef/itemicon/")
    }
    get smallImage() {
        const e = this.image.split("/");
        return e.splice(e.length - 1, 0, "small"),
        e[e.length - 1] = e[e.length - 1].replace(".png", ".webp"),
        e.join("/")
    }
    get nameHash() {
        return this.excel.NameHash
    }
    get role() {
        return this.excel.WeaponType
    }
    get rarity() {
        return this.excel.Rarity
    }
}
var L;
class S1 {
    constructor(e) {
        R(this, L, void 0);
        u(this, L, null),
        this.data = e,
        this.meta = Z0[e.templateid]
    }
    get level() {
        return 0
    }
    stats() {
        const e = this.data.enhance;
        return this.meta.excel.AttrModifiers.map( (t, n) => {
            var c;
            const o = Math.min(n, 3);
            return new ie(t.AttrType,t.Values[((c = e.find(B => B.key == o)) == null ? void 0 : c.value) || 0]).remake(t.Formula)
        }
        )
    }
    get hash() {
        if (s(this, L))
            return s(this, L);
        let e = "";
        return e += "" + this.meta.id + this.level + this.data.enhance.map(i => "" + i.key + i.value).join(""),
        u(this, L, e),
        e
    }
}
L = new WeakMap;
class Q0 {
    constructor(e) {
        this.count = 0,
        this.relics = [],
        this.id = e,
        this.excel = de.Suits[e]
    }
    get nameHash() {
        return this.excel.NameHash
    }
    get icon() {
        return this.excel.Icon
    }
}
class y1 {
    constructor(e) {
        this.id = e;
        const i = de;
        this.excel = i.Items[e],
        this.set = {
            Id: this.excel.SuitId,
            ...i.Suits[this.excel.SuitId]
        }
    }
    get image() {
        return this.excel.Icon
    }
    get smallImage() {
        const e = this.image.split("/");
        return e.splice(e.length - 1, 0, "small"),
        e[e.length - 1] = e[e.length - 1].replace(".png", ".webp"),
        e.join("/")
    }
    get nameHash() {
        return this.set.NameHash
    }
    get rarity() {
        return this.excel.Rarity
    }
}
const K0 = [{
    icon: null,
    color: null
}, {
    icon: null,
    color: "#9B9B9B"
}, {
    icon: null,
    color: "#ABCE42"
}, {
    icon: null,
    color: "#26BBFD"
}, {
    icon: null,
    color: "#9452FA"
}, {
    icon: null,
    color: "#FFBB03"
}, {
    icon: null,
    color: "#FF7100"
}];
class j0 {
    constructor(e) {
        this.type = g.EF,
        this.data = e,
        this.stats = []
    }
    get nickname() {
        return this.data.name || "???"
    }
    get signature() {
        return this.data.signature || ""
    }
    get uid() {
        return this.data.platformRoleId
    }
    get server() {
        return b0.uidToRegion(this.data.platformRoleId)
    }
    get pfp() {
        return M0[this.data.userAvatarId].Icon
    }
    get background() {
        return L0[this.data.businessCardTopicId].Icon.replace("friendlistbg", "businesscardbg").replace(".png", ".webp")
    }
    get level() {
        return this.data.adventureLevel || 1
    }
    get worldLevel() {
        return this.data.worldLevel || 1
    }
    get medals() {
        return this.data.achievement
    }
}
class X0 {
    constructor(e, i, t=null) {
        this.id = e,
        this.value = ""
    }
    get icon() {
        return ""
    }
    get nameHash() {
        return ""
    }
}
const J0 = Object.fromEntries(Object.keys(u1).map(a => [a, new l1(a)]))
  , $0 = Object.fromEntries(Object.keys(s1).map(a => [a, new A1(a)]))
  , Z0 = Object.fromEntries(Object.keys(de.Items).map(a => [a, new y1(a)]));
[y.Atk_base].reduce( (a, e, i) => (a[e] = i,
a), {});
[y.Atk_base].reduce( (a, e, i) => (a[e] = i,
a), {});
const g1 = {
    Avatar: W0,
    AvatarMeta: l1,
    Weapon: d1,
    WeaponMeta: A1,
    Relic: S1,
    RelicMeta: y1,
    PlayerInfo: j0,
    Property: ie,
    Statistic: X0,
    Rarities: K0
};
function Ji(a) {
    let e = null;
    for (let i of a)
        if (Z.TermNums[i.termNumId].TermType == 3) {
            e = Z.TermNums[i.termNumId];
            break
        } else
            e = Z.TermNums[49];
    return e.TagIcon
}
const ei = {
    Physical: "#333",
    Physical_I: "#999",
    Fire: "#f45511",
    Pulse: "#e3b80c",
    Cryst: "#30d6e0",
    Natural: "#b4d945"
}
  , ii = {
    3: "#26BBFD",
    4: "#9452FA",
    5: "#FFBB03",
    6: "#FF7100"
};
function R1(a) {
    switch (a) {
    case g.GI:
        return I1;
    case g.HSR:
        return Fe;
    case g.ZZZ:
        return e1;
    case g.EF:
        return g1;
    default:
        throw new Error(`Unknown hoyo type: ${a}`)
    }
}
var pe = {}
  , ti = Se && Se.__awaiter || function(a, e, i, t) {
    function n(o) {
        return o instanceof i ? o : new i(function(p) {
            p(o)
        }
        )
    }
    return new (i || (i = Promise))(function(o, p) {
        function c(P) {
            try {
                _(t.next(P))
            } catch (d) {
                p(d)
            }
        }
        function B(P) {
            try {
                _(t.throw(P))
            } catch (d) {
                p(d)
            }
        }
        function _(P) {
            P.done ? o(P.value) : n(P.value).then(c, B)
        }
        _((t = t.apply(a, e || [])).next())
    }
    )
}
;
Object.defineProperty(pe, "__esModule", {
    value: !0
});
const B1 = () => P1 || window && (window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB);
let P1;
pe.setIndexedDb = a => {
    P1 = a
}
;
const ai = a => new Promise( (e, i) => {
    const t = B1();
    if (!t) {
        i("indexedDB not supported");
        return
    }
    const n = t.open(a, 1);
    n.onsuccess = function() {
        e(this.result)
    }
    ,
    n.onerror = function(o) {
        i("indexedDB request error"),
        console.error(o)
    }
    ,
    n.onupgradeneeded = function() {
        const o = this.result.createObjectStore("kv-store", {
            keyPath: "k"
        });
        o.transaction.oncomplete = function() {
            e(this.db)
        }
    }
}
);
pe.removeKeyValueStore = a => new Promise( (e, i) => {
    const n = B1().deleteDatabase(a);
    n.onerror = i,
    n.onsuccess = () => e()
}
);
var ni = pe.getKeyValueStore = a => ti(void 0, void 0, void 0, function*() {
    const e = yield ai(a)
      , i = t => e.transaction("kv-store", t).objectStore("kv-store");
    return {
        get: t => new Promise( (n, o) => {
            const p = i("readonly").get(t);
            p.onerror = o,
            p.onsuccess = function() {
                var c, B = (c = this.result) === null || c === void 0 ? void 0 : c.v;
                n(typeof B < "u" ? B : void 0)
            }
        }
        ),
        getKeys: () => new Promise( (t, n) => {
            const o = i("readonly").getAllKeys();
            o.onerror = n,
            o.onsuccess = function() {
                t(this.result.map(p => p.toString()))
            }
        }
        ),
        set: (t, n) => new Promise( (o, p) => {
            const c = i("readwrite").put({
                k: t,
                v: n
            });
            c.onsuccess = () => o(),
            c.onerror = p
        }
        ),
        remove: t => new Promise( (n, o) => {
            const p = i("readwrite").delete(t);
            p.onsuccess = () => n(),
            p.onerror = o
        }
        ),
        clear: () => new Promise( (t, n) => {
            const o = i("readwrite").clear();
            o.onsuccess = () => t(),
            o.onerror = n
        }
        )
    }
});
async function ue() {
    let a = null;
    try {
        a = await ni("builds")
    } catch {
        console.error("Storage not available here.")
    }
    return a
}
var T1 = (a, e, i) => {
    if (!e.has(a))
        throw TypeError("Cannot " + i)
}
, he = (a, e, i) => (T1(a, e, "read from private field"),
i ? i.call(a) : e.get(a)), oi = (a, e, i) => {
    if (e.has(a))
        throw TypeError("Cannot add the same private member more than once");
    e instanceof WeakSet ? e.add(a) : e.set(a, i)
}
, pi = (a, e, i, t) => (T1(a, e, "write to private field"),
t ? t.call(a, i) : e.set(a, i),
i), Y;
const h1 = class T extends D1 {
    constructor(e) {
        super(e),
        oi(this, Y, "");
        const i = R1(this.data.hoyo_type);
        this.avatar = new i.Avatar(this.avatar_data)
    }
    get id() {
        return this.data.id
    }
    get hoyo_profile() {
        return this.data.hoyo_profile
    }
    get name() {
        return this.data.name
    }
    get avatar_id() {
        return this.data.avatar_id
    }
    get avatar_data() {
        return this.data.avatar_data
    }
    get live() {
        return this.data.live
    }
    get hidden() {
        return this.data.hidden
    }
    get settings() {
        return this.data.settings
    }
    get public() {
        return this.data.public
    }
    get order() {
        return this.data.order
    }
    get image() {
        var e;
        return (e = this.data.image) == null ? void 0 : e.replace("minio:9087/", "localhost:5173/")
    }
    get image_hash() {
        return this.data.image_hash
    }
    get hoyo_type() {
        return this.data.hoyo_type
    }
    get changed_at() {
        return this.data.changed_at
    }
    get hoyo() {
        return this.data.hoyo
    }
    get owner() {
        return this.data.owner
    }
    get hash() {
        var i;
        if (performance.now(),
        he(this, Y))
            return he(this, Y);
        let e = "";
        return this.avatar && (e += this.avatar.hash,
        e += this.avatar.relics.map(t => (t == null ? void 0 : t.hash) || "").join(""),
        e += ((i = this.avatar.weapon) == null ? void 0 : i.hash) || ""),
        pi(this, Y, e),
        e
    }
    get link() {
        return `/u/${this.owner}/${this.hoyo}/${this.avatar_id}/${this.id}/`
    }
    get localKey() {
        return `local.build${this.id}.image`
    }
    async getLocalImage() {
        T.indexedDB || (T.indexedDB = await ue());
        const e = await T.indexedDB.get(this.localKey);
        if (e)
            return URL.createObjectURL(e)
    }
    async save(e) {
        return T.create({
            id: this.id,
            hoyo: this.hoyo
        }, {
            name: e
        })
    }
    async imageUpload(e) {
        const i = await new Promise(n => e.toBlob(n))
          , t = new DataTransfer;
        t.items.add(new File([i],"_.png")),
        await T.endpoints.image.request({
            hoyo: this.hoyo,
            id: this.id
        }, {
            image: t.files[0]
        }, {
            throw: !0
        })
    }
    async imageLocalSave(e, i=this.data) {
        const t = await ue()
          , n = await new Promise(o => e.toBlob(o));
        await t.set(this.localKey, n)
    }
    async imageLocalDelete(e=this.data) {
        await (await ue()).remove(this.localKey)
    }
    async imageDelete(e=this.data) {
        await T.endpoints.imageDelete.request({
            hoyo: this.hoyo,
            id: this.id
        }, null, {
            throw: !0
        }),
        await this.refresh()
    }
    async reorder(e, i) {
        const t = await T.endpoints.reorder.request({
            hoyo: this.hoyo,
            id: this.id
        }, {
            right_id: i,
            left_id: e
        });
        return Object.assign(this.data, t.data),
        this.data = this.data,
        t
    }
    static async refresh(e) {
        const i = await this.endpoints.refresh.request({
            hoyo: e
        }, null, {
            throw: !0
        });
        return Object.fromEntries(Object.entries(i.data).map( ([t,n]) => [t, n.map(o => new T(o))]))
    }
    static mergeBAM(e, i) {
        const t = {};
        for (var n in e) {
            const p = e[n];
            for (var o = 0; o < p.length; o++) {
                const c = p[o];
                t[c.id] = [p, o]
            }
        }
        for (var n in i) {
            const c = i[n];
            for (var o = 0; o < c.length; o++) {
                const _ = c[o]
                  , P = t[_.id];
                if (P) {
                    const [d,m] = P;
                    d[m] = _
                } else
                    e[_.avatar_id] || (e[_.avatar_id] = []),
                    e[_.avatar_id].push(_)
            }
        }
    }
}
;
Y = new WeakMap;
h1.indexedDB = null;
let $i = h1;
class ee extends C1 {
    constructor(e) {
        super(e);
        const i = R1(this.hoyo_type);
        this.player_info = new i.PlayerInfo(e.player_info)
    }
    get id() {
        return this.data.id
    }
    get hash() {
        return this.data.hash
    }
    get user() {
        return this.data.user
    }
    get uid() {
        return this.data.uid
    }
    get verified() {
        return this.data.verified
    }
    get public() {
        return this.data.public
    }
    get uid_public() {
        return this.data.uid_public
    }
    get live_public() {
        return this.data.live_public
    }
    get verification_code() {
        return this.data.verification_code
    }
    get verification_expire() {
        return this.data.verification_expire
    }
    get verification_code_retries() {
        return this.data.verification_code_retries
    }
    get avatar_order() {
        return this.data.avatar_order
    }
    get hoyo_type() {
        return this.data.hoyo_type
    }
    get order() {
        return Number(this.data.order)
    }
    get region() {
        return this.data.region
    }
    get refreshed_at() {
        return this.data.refreshed_at
    }
    get live_data_hash() {
        return this.data.live_data_hash
    }
    get ttl() {
        const e = new Date(this.refreshed_at).getTime()
          , i = Date.now();
        return Math.floor(Math.max(0, 60 - (i - e) / 1e3))
    }
    async refreshProfile() {
        const e = await ee.endpoints.refreshProfile.request({
            hash: this.hash
        }, null, {
            throw: !0
        });
        this.data = e.data
    }
    async refreshCode() {
        const e = await ee.endpoints.refreshCode.request({
            hash: this.hash
        }, null, {
            throw: !0
        });
        this.data = e.data
    }
    async reorder(e, i) {
        const t = await ee.endpoints.reorder.request({
            hash: this.hash
        }, {
            right_id: i,
            left_id: e
        });
        return Object.assign(this.data, t.data),
        this.data = this.data,
        t
    }
}

