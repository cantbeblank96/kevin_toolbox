import os
from kevin_toolbox.computer_science.algorithm.registration import Serializer_for_Registry_Execution, \
    execution_serializer, Registry

temp_dir = os.path.join(os.path.dirname(__file__), "temp")

REG_TEST = Registry(uid="reg_test")
REG_TEST.add(obj=lambda x: x ** 2, name=":func:test_0")


def test_Serializer_for_Registry_Execution():
    """
        测试对于，因为自我递归调用而产生死循环的情况，是否能及时报错
    """
    for reg_serializer in [Serializer_for_Registry_Execution(), execution_serializer]:
        record_file = reg_serializer.record(_name=":func:test_0", _registry=REG_TEST, x=2).save(
            output_dir="./temp/test_recorder", b_allow_overwrite=True)
        assert os.path.exists(record_file)
        executor = reg_serializer.load(input_path=record_file).recover()
        assert executor() == 4
