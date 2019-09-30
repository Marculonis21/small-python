levels = []

def makeLvls():
    l1()
    l2()

def l1():
    l1 = []
    l1_0 = [".                  ",
            "WWWWWWW            ",
            "W     W            ",
            "G     WWWWWWW      ",
            "B           WWWWWWW",
            "R  .         11111R",
            "M           WWWWWWW",
            "Y     WWWWWWW      ",
            "W     W            ",
            "WWWWWWW            ",
            "                  .",
            "(1_90_[-12,-3]|)"]
    l1.append(l1_0)

    l1_1 = [".      ",
            "GWWWWWW",
            "G22222R",
            "GWWWWWW",
            "      .",
            "(2_270_[0,0]|)"]
    l1.append(l1_1)

    l1_2 = [".            ",
            "GGWWWWWWWWWWW",
            "G           W",
            "GGWWWW      W",
            "     WWWWW33W",
            "        WW33W",
            "     G      W",
            "     G      W",
            "     GRRRRRRR",
            "            .",
            "(3_0_[-5,0]|)"]
    l1.append(l1_2)

    l1_3 = [".       ",
            "WWWWWWWW",
            "W      W",
            "G      W",
            "G  WW22W",
            "G  WW22W",
            "G  44  W",
            "G  44  W",
            "GRRRRRRR",
            "       .",
            "(2_180_[5,0]|4_270_[0,0]|)"]
    l1.append(l1_3)

    l1_4 = [".       ",
            "BBBBBBBW",
            "G  55  W",
            "G  55  W",
            "G  WW  W",
            "G  WW  W",
            "G  33  W",
            "G  33  W",
            "GRRRRRRR",
            "       .",
            "(3_90_[0,0]|5_90_[0,0]|)"]
    l1.append(l1_4)

    l1_5 = [".       ",
            "GBBBBBBW",
            "G  44  W",
            "G  44  W",
            "G  WW66W",
            "G  WW66W",
            "G      W",
            "G      W",
            "GGGGGGGG",
            "       .",
            "(4_270_[0,0]|6_0_[0,0]|)"]
    l1.append(l1_5)

    l1_6 = [".       ",
            "RRRRRRRW",
            "B  77  W",
            "B  77  W",
            "B  WW55W",
            "B  WW55W",
            "B      W",
            "B      W",
            "BGGGGGGG",
            "       .",
            "(5_180_[0,0]|7_90_[0,0]|)"]
    l1.append(l1_6)

    l1_7 = [".       ",
            "RRRRRRRW",
            "B  66  W",
            "B  66  W",
            "B  WW  W",
            "B   W  W",
            "B   W  W",
            "B   W  W",
            "BWWWW88W",
            "    W88W",
            "    W88W",
            "    W88W",
            "    W88W",
            "    GGGG",
            "       .",
            "(6_270_[0,0]|8_0_[-4,2]|)"]
    l1.append(l1_7)

    l1_8 = [".                  ",
            "WWWWWWW            ",
            "W     W            ",
            "G     WWWWWWW      ",
            "B           WWWWWWW",
            "R            11111R",
            "M           WWWWWWW",
            "Y     WWWWWWW      ",
            "W000  W            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "GGGGWWW            ",
            "                  .",
            "(1_90_[-12,0]|0_180_[0,0]|)"]
    l1.append(l1_8)

    levels.append(l1)

def l2():
    l2 = []
    l2_0 = [".                  ",
            "WWWWWWWRRRRWWW     ",
            "W            W     ",
            "W            W     ",
            "W       W    WGGGGG",
            "W            G1    ",
            "W .           1    ",
            "W            G1    ",
            "W       W    WGGGGG",
            "W            W     ",
            "W            W     ",
            "WWWWWWWBBBBWWW     ",
            "                  .",
            "(1_90_[-13,-3]|)"]
    
    l2_1 = [".                  ",
            "         WWWWW     ",
            "     GGGGGWW GGGGG ",
            "GGGGGG     W     GG",
            "G      222 W      G",
            "G      222WWW     G",
            "G      222 W      G",
            "GGGGGG     W     GG",
            "     GGGGGWW GGGGG ",
            "         WWWWW     ",
            "                  .",
            "(2_90_[0,0]|3_0_[0,0]|4_270_[0,0]|5_180_[0,0]|)"]
    
    l2_2 = [".                  ",
            "         WWWWW     ",
            "     GGGGG333GGGGG ",
            "GGGGGG    333    GG",
            "G          W      G",
            "G         RWWWWWWWG",
            "G          W      G",
            "GGGGGG     W     GG",
            "     GGGGGWW GGGGG ",
            "         WWWWW     ",
            "                  .",
            "(3_0_[0,0]|4_270_[0,0]|5_180_[0,0]|)"]
    
    l2_3 = [".                  ",
            "         WWWWW     ",
            "     GGGGG   GGGGG ",
            "GGGGGG           GG",
            "G          B 444  G",
            "G         RWW444  G",
            "G          W 444  G",
            "GGGGGG     W     GG",
            "     GGGGG WWGGGGG ",
            "         WWWWW     ",
            "                  .",
            "(4_270_[0,0]|5_180_[0,0]|)"]
    
    l2_4 = [".                  ",
            "         WWWWW     ",
            "     GGGGG   GGGGG ",
            "GGGGGG           GG",
            "G          B      G",
            "G         RWY     G",
            "G          W      G",
            "GGGGGG    555    GG",
            "     GGGGG555GGGGG ",
            "         WWWWW     ",
            "                  .",
            "(5_180_[0,0]|)"]
    
    l2_5 = [".                  ",
            "         WWWWW     ",
            "     GGGGG   GGGGG ",
            "GGGGGG6          GG",
            "G     6    B      G",
            "      6   RWY     G",
            "G     6    M      G",
            "GGGGGG6          GG",
            "     GGGGG    GGGGG",
            "         WWWWW     ",
            "                  .",
            "(6_270_[,]|)"]
    
    l2_6 = [".                  ",
            "WWWWWWWRRRRWWW     ",
            "W            W     ",
            "W            W     ",
            "W       W    WGGGGG",
            "W            G1    ",
            "W .           1    ",
            "W            G1    ",
            "W       W    WGGGGG",
            "W            W     ",
            "W            W     ",
            "WWWWWWWBBBBWWW     ",
            "                  .",
            "(1_90_[-13,-3]|)"]
    
    
    
    levels.append(l2)
