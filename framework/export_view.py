#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
# Author: Lee <lee@chengantech.com>
# Date: 2018-03-13

import json
from io import BytesIO
from urllib.parse import quote, unquote

from flask import request, jsonify, abort, send_file
from flask.views import MethodView
import pandas as pd


class ExportView(MethodView):
    """
    ExportView

    export the list data as excel

    EXPORT_DICT = {
        'filename': 'contact_list.xlsx',
        'ret_rule': ('data', 'detail'),
        'export_rule': (
            {'key_name': 'chinese_name',  'field_name': '联系人'},
            {'key_name': 'tag_data[].tag_name', 'field_name': '类型'},
            {'key_name': 'phone', 'field_name': '联系电话'},
            {'key_name': 'email', 'field_name': '联系邮箱'},
            {'key_name': 'address', 'field_name': '所在地'},
            {'key_name': 'dt_create', 'field_name': '创建时间 '},
            {'key_name': 'creator_name', 'field_name': '录入人员'},
        ),
    }

    key_name 中的[]表示该字段是个列表, field_name 为表头展示字段
    """

    EXPORT_DICT = {
        'filename': 'download.xlsx',
        'ret_rule': (),
        'export_rule': (),
    }

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        if request.method == 'POST':
            j = request.get_json()
            if j is not None:
                if j.get('is_download', False):
                    return self._trans_params()
        return meth(*args, **kwargs)

    def get(self):
        params = request.args.get('export_params')
        if params is None:
            abort(404, '文件不存在')
        params = json.loads(unquote(params))
        if params.get('is_download'):
            del params['is_download']
        else:
            abort(405, 'Method not Allowed')
        params['page_num'] = 1
        params['page_size'] = 999

        dataset = self.post(params)
        ret_data = self._export_wrapper(dataset)
        return send_file(ret_data,
                         attachment_filename=self.EXPORT_DICT['filename'],
                         as_attachment=True)

    def _trans_params(self):
        script_root = request.script_root
        path = request.path
        base_url = script_root + path
        ret_url = base_url + \
            '?export_params={0}'.format(quote(json.dumps(request.get_json())))
        ret = {
            'errcode': 0,
            'errmsg': 'OK',
            'data': {
                'file_url': ret_url,
            }
        }
        return jsonify(ret)

    def _export_wrapper(self, data):
        # 获取详情列表
        data_list = data.data.decode('utf-8')
        data_list = json.loads(data_list)
        for k in self.EXPORT_DICT['ret_rule']:
            data_list = data_list.get(k)
        # 空数据只返回表头
        if len(data_list) == 0:
            df = pd.DataFrame(columns=[d['field_name'] for d in self.EXPORT_DICT['export_rule']])
            f = BytesIO()
            writer = pd.ExcelWriter(f, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='导出详情', index=False)
            writer.save()
            f.seek(0)
            return f

        # 抽取列表形式
        for k in self.EXPORT_DICT['export_rule']:
            if '.' not in k['key_name']:
                continue
            # XXX 此处只限两层
            foo_list, foo_dict = k['key_name'].split('.')
            if '[]' in foo_list:
                foo_list = foo_list[:-2]
                for foo_data in data_list:
                    foo_data[foo_list] = ','.join([str(d[foo_dict]) for d in foo_data[foo_list]])
                    foo_data[k['key_name']] = foo_data[foo_list]
            else:
                for foo_data in data_list:
                    foo_data[k['key_name']] = foo_data[foo_list][foo_dict]
        # 清理空数据
        for foo_data in data_list:
            for k, v in foo_data.items():
                if isinstance(v, str):
                    foo_str = ''.join(v.split()).replace(',', '').replace('|', '')
                    if len(foo_str) == 0:
                        foo_data[k] = ''

        # 准备导出数据
        foo_df = pd.DataFrame(data_list)
        df = foo_df[[d['key_name'] for d in self.EXPORT_DICT['export_rule']]]
        df.columns = [d['field_name'] for d in self.EXPORT_DICT['export_rule']]

        # 导出数据
        f = BytesIO()
        writer = pd.ExcelWriter(f, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='导出详情', index=False)
        writer.save()
        f.seek(0)
        return f
