
from app.common.database.objects import DBScore
from app.common.constants import GameMode, Mods

from akatsuki_pp_py import Calculator, Beatmap

from typing import Optional

import app

def total_hits(score: DBScore) -> int:
    if score.mode == GameMode.CatchTheBeat:
        return score.n50 + score.n100 + score.n300 + score.nMiss + score.nKatu

    elif score.mode == GameMode.OsuMania:
        return score.n300 + score.n100 + score.n50 + score.nGeki + score.nKatu + score.nMiss

    return score.n50 + score.n100 + score.n300 + score.nMiss

def calculate_ppv2(score: DBScore) -> Optional[float]:
    beatmap_file = app.session.storage.get_beatmap(score.beatmap_id)

    if not beatmap_file:
        app.session.logger.error(
            f'pp calculation failed: Beatmap file was not found! ({score.user_id})'
        )
        return

    bm = Beatmap(bytes=beatmap_file)

    calc = Calculator(
        mode           = score.mode,
        mods           = score.mods,
        acc            = score.acc,
        n_geki         = score.nGeki,
        n_katu         = score.nKatu,
        n300           = score.n300,
        n100           = score.n100,
        n50            = score.n50,
        n_misses       = score.nMiss,
        combo          = score.max_combo,
        passed_objects = total_hits(score)
    )

    if not (result := calc.performance(bm)):
        return

    mods = Mods(score.mods)
    pp = result.pp

    if score.mode == 1 and Mods.Relax in mods:
        # Remove the color attribute when playing relax
        pp = pp / max(1, result.difficulty.color)

    return pp
