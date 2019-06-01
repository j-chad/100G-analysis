from copy import copy
from pathlib import Path

import pandas

if __name__ == "__main__":
    df = pandas.read_csv(Path("../survey_results_public.csv"), index_col="Respondent")
    multiColumns = [
        "LanguageWorkedWith", "LanguageDesireNextYear",
        "DatabaseWorkedWith", "DatabaseDesireNextYear",
        "PlatformWorkedWith", "PlatformDesireNextYear",
        "WebFrameWorkedWith", "WebFrameDesireNextYear",
        "MiscTechWorkedWith", "MiscTechDesireNextYear"
    ]
    for i in multiColumns:
        sf = df.copy()
        s = sf[i].str.split(";").apply(pandas.Series, 1).stack()
        s.index = s.index.droplevel(-1)
        s.name = i
        print(f"Done: {i}")
        s.to_csv(Path(f"../survey_results_public_{i}_modified.csv"), header=True, index=True)
