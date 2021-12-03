# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-节点管理(BlueKing-BK-NODEMAN) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import abc
from functools import wraps
from typing import Dict, List, Set, Union

from ..base import BaseService, CommonData


class AgentBaseService(BaseService, metaclass=abc.ABCMeta):
    """
    AGENT安装基类
    """

    def sub_inst_failed_handler(self, sub_inst_ids: Union[List[int], Set[int]]):
        """
        订阅实例失败处理器
        :param sub_inst_ids: 订阅实例ID列表/集合
        """
        pass


class AgentCommonData(CommonData):
    def __init__(self, sub_inst_id__host_id_map: Dict[int, int], **kwargs):
        self.sub_inst_id__host_id_map = sub_inst_id__host_id_map
        super().__init__(**kwargs)


def batch_call_single_exception_handler(single_func):
    # 批量执行时单个机器的异常处理
    @wraps(single_func)
    def wrapper(self, sub_inst_id, *args, **kwargs):
        try:
            return single_func(self, sub_inst_id, *args, **kwargs)
        except Exception as error:
            self.move_insts_to_failed([sub_inst_id], error)

    return wrapper
