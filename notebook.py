import marimo

__generated_with = "0.11.29"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""# PAKW""")
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import math
    return math, mo, pd


@app.cell
def _(pd):
    db = pd.read_json("db.json")
    return (db,)


@app.cell
def _(db, mo):
    state_cat = db["NEGERI"].unique()
    state = mo.ui.dropdown(state_cat, label="Negeri:")
    state
    return state, state_cat


@app.cell
def _(db, mo, state):
    if state.value:
        district_cat = db[db["NEGERI"] == state.value]["DAERAH"].unique()
    else:
        district_cat = []
    district = mo.ui.dropdown(district_cat, label="Daerah:")
    district
    return district, district_cat


@app.cell
def _(db, district, mo):
    if district.value:
        strata_cat = db[db["DAERAH"] == district.value]["STRATA"].unique()
    else:
        strata_cat = []
    strata = mo.ui.dropdown(strata_cat, label="Strata:")
    strata
    return strata, strata_cat


@app.cell
def _(mo):
    jumlah_isi = mo.ui.number(start=1, step=1, label="Jumlah Isi Rumah:")
    jumlah_isi
    return (jumlah_isi,)


@app.cell
def _(db):
    age_cat = db["UMUR_KSH"].unique()
    gender_cat = db["JANTINA"].unique()
    return age_cat, gender_cat


@app.cell
def _(mo):
    def person(age_cat, gender_cat):
        return mo.ui.dictionary(
            {
                "age": mo.ui.dropdown(age_cat, label="Umur:"),
                "gender": mo.ui.dropdown(gender_cat, label="Jantina:"),
            },
            label=" ",
        )
    return (person,)


@app.cell
def _(age_cat, gender_cat, jumlah_isi, person):
    isi_rumah_ = {}

    for i in range(jumlah_isi.value):
        isi_rumah_[f"person-{i+1}"] = person(age_cat, gender_cat)
    return i, isi_rumah_


@app.cell
def _(isi_rumah_, mo):
    isi_rumah = mo.ui.dictionary(isi_rumah_, label="Ahli Isi Rumah")
    isi_rumah
    return (isi_rumah,)


@app.cell
def _(district, state, strata):
    filter_dict = {
        "NEGERI": state.value,
        "DAERAH": district.value,
        "STRATA": strata.value,
    }
    return (filter_dict,)


@app.cell
def _(db, filter_dict):
    filt_dict = db.copy()

    for k, v in filter_dict.items():
        if v:
            # print(k, v)
            filt_dict = filt_dict[filt_dict[k] == v]

    # if age.value and gender.value:
    #     filt_dict = filt_dict[filt_dict["UMUR_KSH"] == age.value]
    #     filt_dict = filt_dict[filt_dict["JANTINA"] == gender.value]
    return filt_dict, k, v


@app.cell
def _(filt_dict, isi_rumah, jumlah_isi, math):
    def calc(filt_dict=filt_dict, isi_rumah=isi_rumah):
        makanan = 0
        makan_luar = 0
        rent = 0
        lain = 0
        for kk, vv in isi_rumah.items():
            if vv["age"].value and vv["gender"].value:
                filt_dict_copy = filt_dict.copy()
                filt_dict_copy = filt_dict_copy[
                    filt_dict_copy["UMUR_KSH"] == vv["age"].value
                ]
                filt_dict_copy = filt_dict_copy[
                    filt_dict_copy["JANTINA"] == vv["gender"].value
                ]

                rent += filt_dict_copy["Mean_p_rent"].values[0]
                makan_luar = filt_dict_copy["Kos_makan_luar"].values[0]
                makanan += filt_dict_copy["Mean_TOTAL_PAKW_MAKANAN"].values[0]
                lain += filt_dict_copy["Mean_p_lain2"].values[0]

        avg_mean_rent = rent / jumlah_isi.value
        adj_avg_mean_rent = avg_mean_rent * math.pow(jumlah_isi.value, 0.4745)
        total_pakw = (
            (((makanan + 30) * 1.05 * makan_luar) + 131) + lain + adj_avg_mean_rent
        )
        perkapita = total_pakw / jumlah_isi.value
        return {
            "makanan": makanan,
            "makan_luar": makan_luar,
            "rent": rent,
            "lain": lain,
            "total_pakw": total_pakw,
            "perkapita": perkapita,
        }
    return (calc,)


@app.cell
def _(calc, mo):
    mo.callout(calc(), kind="info")
    return


if __name__ == "__main__":
    app.run()
