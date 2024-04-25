from pandera import DataFrameSchema, Column, Check, Index, MultiIndex

schema = DataFrameSchema(
    columns={
        "Temperatura_do_Ar": Column(
            dtype="float64",
            checks= Check(lambda x: x>=0),
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Temperatura_do_Motor": Column(
            dtype="float64",
            checks= Check(lambda x: x>=0),
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "RPM_Motor": Column(
            dtype="float64",
            checks= Check(lambda x: x>=0),
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Vibracao_do_Motor": Column(
            dtype="float64",
            checks= Check(lambda x: x>=0),
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "Torque": Column(
            dtype="float64",
            checks= Check(lambda x: x>=0),
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
    },
    checks=None,
    index=Index(
        dtype="int64",
        checks=None,
        nullable=False,
        coerce=False,
        name=None,
        description=None,
        title=None,
    ),
    dtype=None,
    coerce=False,
    strict="filter",
    name=None,
    ordered=True,
    unique=None,
    report_duplicates="all",
    unique_column_names=False,
    add_missing_columns=False,
    title=None,
    description=None,
)