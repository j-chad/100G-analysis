from pathlib import Path

import pandas

if __name__ == "__main__":
    df = pandas.read_csv(Path("../survey_results_public.csv"))
    multiColumns = [
        "LanguageWorkedWith", "LanguageDesireNextYear",
        "DatabaseWorkedWith", "DatabaseDesireNextYear",
        "PlatformWorkedWith", "PlatformDesireNextYear",
        "WebFrameWorkedWith", "WebFrameDesireNextYear",
        "MiscTechWorkedWith", "MiscTechDesireNextYear"
    ]
    for i in multiColumns:
        s = df[i].str.split(";").apply(pandas.Series, 1).stack()
        s.index = s.index.droplevel(-1)
        s.name = i
        del df[i]
        df.join(s)
        print(f"Done: {i}")
    df.to_csv(Path("../survey_results_public_modified.csv"))
