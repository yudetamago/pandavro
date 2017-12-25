import pytest
import numpy as np
import pandas as pd
import pandavro as pdx
from tempfile import NamedTemporaryFile
from pandas.util.testing import assert_frame_equal
from io import BytesIO


@pytest.fixture
def dataframe():
    return pd.DataFrame({"String": ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar'],
                         "Float64": np.random.randn(8),
                         "Int64": np.random.randint(0, 10, 8),
                         "Boolean": [True, False, True, False, True, False, True, False]
                         })


def test_schema_infer(dataframe):
    expect = {
        'type': 'record',
        'name': 'Root',
        'fields':
            [
                {'type': ['null', 'boolean'], 'name': 'Boolean'},
                {'type': ['null', 'double'], 'name': 'Float64'},
                {'type': ['null', 'long'], 'name': 'Int64'},
                {'type': ['null', 'string'], 'name': 'String'}
            ]
    }
    assert expect == pdx.__schema_infer(dataframe)


def test_fields_infer(dataframe):
    expect = [
        {'type': ['null', 'boolean'], 'name': 'Boolean'},
        {'type': ['null', 'double'], 'name': 'Float64'},
        {'type': ['null', 'long'], 'name': 'Int64'},
        {'type': ['null', 'string'], 'name': 'String'}
    ]
    assert expect == pdx.__fields_infer(dataframe)


def test_buffer_e2e(dataframe):
    tf = NamedTemporaryFile()
    pdx.to_avro(tf.name, dataframe)
    with open(tf.name, 'rb') as f:
        expect = pdx.from_avro(BytesIO(f.read()))
    assert_frame_equal(expect, dataframe)
    f.close()


def test_file_path_e2e(dataframe):
    tf = NamedTemporaryFile()
    pdx.to_avro(tf.name, dataframe)
    expect = pdx.from_avro(tf.name)
    assert_frame_equal(expect, dataframe)


if __name__ == '__main__':
    pytest.main()
