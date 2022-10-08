﻿from FontEffects import colours

LOGO_TREKER_PREFIX = [colours.fg.orange]
LOGO_TREKER_SUFFIX = [colours.reset]
LOGO_TREKER_TEXT = r"""
               ______ _______ ______ ______    _______ ______  ______ __  __ 
              / __  //__  __// __  // __  /   /__  __// __  / / ____// / / /
             / / /_/   / /  / /_/ // /_/ /      / /  / /_/ / / /__  / // /
             _\ \     / /  / __  //   __/      / /  /   __/ / __ / /   / 
           / /_/ /   / /  / / / // /\ \       / /  / /\ \  / /___ / /\ \
          /_____/   /_/  /_/ /_//_/  \_\     /_/  /_/  \_\/_____//_/  \_\

                                     1971 - 2020                                 """.split('\n')
LOGO_TREKER_SHIP = r"""
                           ________________        _
                           \__(=======/_=_/____.--'-`--.___
                                      \ \   `,--,-.___.----'
                                    .--`\\--'../
                                   '---._____.|]""".split('\n')

LOGO_TREKER  = LOGO_TREKER_PREFIX + LOGO_TREKER_TEXT + LOGO_TREKER_SUFFIX + LOGO_TREKER_SHIP

AREA_NAMES = [
    "Aaamazzara",
    "Altair IV",
    "Aurelia",
    "Bajor",
    "Benthos",
    "Borg Prime",
    "Cait",
    "Cardassia Prime",
    "Cygnia Minor",
    "Daran V",
    "Duronom",
    "Dytallix B",
    "Efros",
    "El-Adrel IV",
    "Epsilon Caneris III",
    "Ferenginar",
    "Finnea Prime",
    "Freehaven",
    "Gagarin IV",
    "Gamma Trianguli VI",
    "Genesis",
    "H'atoria",
    "Holberg 917-G",
    "Hurkos III",
    "Iconia",
    "Ivor Prime",
    "Iyaar",
    "Janus VI",
    "Jouret IV",
    "Juhraya",
    "Kabrel I",
    "Kelva",
    "Ktaris",
    "Ligillium",
    "Loval",
    "Lyshan",
    "Magus III",
    "Matalas",
    "Mudd",
    "Nausicaa",
    "New Bajor",
    "Nova Kron",
    "Ogat",
    "Orion III",
    "Oshionion Prime",
    "Pegos Minor",
    "P'Jem",
    "Praxillus",
    "Qo'noS",
    "Quadra Sigma III",
    "Quazulu VIII",
    "Rakosa V",
    "Rigel VII",
    "Risa",
    "Romulus",
    "Rura Penthe",
    "Sauria",
    "Sigma Draconis",
    "Spica",
    "Talos IV",
    "Tau Alpha C",
    "Ti'Acor",
    "Udala Prime",
    "Ultima Thule",
    "Uxal",
    "Vacca VI",
    "Volan II",
    "Vulcan",
    "Wadi",
    "Wolf 359",
    "Wysanti",
    "Xanthras III",
    "Xendi Sabu",
    "Xindus",
    "Yadalla Prime",
    "Yadera II",
    "Yridian",
    "Zalkon",
    "Zeta Alpha II",
    "Zytchin III",
    ]

HELM_CMDS = [
    "--- Commands -----------------",
    "nav = Warp Speed      srs = Short Range Scan  tor = Photon Torpedos",
    "sub = Sublight Speed  lrs = Long Range Scan   pha = Phasers",
    "qui = Quit            com = Access Computer   she = Shields",
    ]

CPU_CMDS = [
    "--- Main Computer --------------",
    "rec = Cumulative Galatic Record",
    "sta = Status Report",
    "tor = Photon Torpedo Targets",
    "bas = Starbase Locations",
    ]