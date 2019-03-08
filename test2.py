# -*- coding:utf-8 -*-
import os, shutil


def file_copy(old_file, new_file):
    if os.path.isfile(old_file):
        try:
            if not os.path.exists(os.path.split(new_file)[0]):
                os.makedirs(os.path.split(new_file)[0])
            shutil.copy(old_file, new_file)
            return True
        except Exception as e:
            return False
    else:
        return False


if __name__ == '__main__':
    all_file = [['C:/Users/tlju/Desktop/所有操作手册/0资产管理系统与财务管理系统应用集成用户操作手册V2.0--项目和投资计划信息下达.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/项目信息和投资计划信息/(1-5)-0资产管理系统与财务管理系统应用集成用户操作手册V2.0--项目和投资计划信息下达.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/(资产)接收项目前期费资金支付.doc', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/项目信息和投资计划信息/(6)-(资产)接收项目前期费资金支付.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/1资产管理系统与财务管理系统应用集成用户操作手册V2.0--工程业务报销支付.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/工程业务报销／付款/(7-15)-1资产管理系统与财务管理系统应用集成用户操作手册V2.0--工程业务报销支付.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/物资合同签订-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/物资业务报销支付/(16-17)-物资合同签订-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/物资发票登记-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/物资业务报销支付/(18)-物资发票登记-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/物资付款申请结果反馈-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/物资业务报销支付/(19-20)-物资付款申请结果反馈-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/物资成本归集-协同场景操作手册.doc', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/物资业务报销支付/(21)-物资成本归集-协同场景操作手册.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/3资产管理系统与财务管理系统应用集成用户操作手册V2.0--工程建设阶段帐卡物一致.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/工程建设阶段帐卡物一致/(22-28)-3资产管理系统与财务管理系统应用集成用户操作手册V2.0--工程建设阶段帐卡物一致.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/资产财务-工程建设阶段帐卡物一致-协同场景操作手册2018-08-30.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/工程建设阶段帐卡物一致/(22-28)-资产财务-工程建设阶段帐卡物一致-协同场景操作手册2018-08-30.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/物资出入库-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/物资采购阶段账卡物一致/(29-30)-物资出入库-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步物资盘点数据信息-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/物资采购阶段账卡物一致/(31)-同步物资盘点数据信息-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步物资调拨数据信息-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/物资采购阶段账卡物一致/(32)-同步物资调拨数据信息-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/资产财务-运维检修阶段帐卡物一致-维护检修管理-协同场景操作手册2018-08-30.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/运维检修阶段帐卡物一致/(33-44)-资产财务-运维检修阶段帐卡物一致-维护检修管理-协同场景操作手册2018-08-30.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/资产财务-运维检修阶段帐卡物一致-协同场景操作手册2018-08-30.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/运维检修阶段帐卡物一致/(33-44)-资产财务-运维检修阶段帐卡物一致-协同场景操作手册2018-08-30.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/资产财务-退役报废阶段帐卡物一致-协同场景操作手册2015-08-07.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/退役报废阶段帐卡物一致/(45-50)-资产财务-退役报废阶段帐卡物一致-协同场景操作手册2015-08-07.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步物资报废入库数据信息-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/退役报废阶段帐卡物一致/(51)-同步物资报废入库数据信息-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步物资报废出库数据信息-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/退役报废阶段帐卡物一致/(52)-同步物资报废出库数据信息-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/公网通信资源-协同场景操作手册V1.0.doc', 'C:/Users/tlju/Desktop/230场景操作手册/资产－财务/其他/(53)-公网通信资源-协同场景操作手册V1.0.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/工资薪酬支付流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/人资－财务/人资资金支付/(57-58)-工资薪酬支付流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/住房公积金支付流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/人资－财务/人资资金支付/(61-62)-住房公积金支付流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/企业年金支付流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/人资－财务/人资资金支付/(63-64)-企业年金支付流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/会计报表流程场景-协同场景操作手册V2.0.docx', 'C:/Users/tlju/Desktop/230场景操作手册/人资－财务/人资会计报表/(65-66)-会计报表流程场景-协同场景操作手册V2.0.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/计量物资入库流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/计量物资出入库/(79-85)-计量物资入库流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/计量物资再利用入库流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/计量物资出入库/(86-87)-计量物资再利用入库流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/计量物资报废入库流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/计量物资出入库/(88)-计量物资报废入库流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/计量物资退库流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/计量物资出入库/(89)-计量物资退库流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/计量物资领用出库流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/计量物资出入库/(90-91)-计量物资领用出库流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/计量物资移库流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/计量物资出入库/(92-93)-计量物资移库流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/计量物资调拨流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/计量物资出入库/(94-95)-计量物资调拨流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/合同签订流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/物资合同主数据/(96)-合同签订流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/合同变更流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/物资合同主数据/(97)-合同变更流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/合同终止流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/物资合同主数据/(98)-合同终止流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/零星采购签订流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/资产-营销/物资合同主数据/(99)-零星采购签订流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/快速复电-班组填报操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网故障抢修/(117-118)-快速复电-班组填报操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/快速复电 - 客服报障-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网故障抢修/(119)-快速复电 - 客服报障-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/线损异常处理-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/运维问题管理/(153-162)-线损异常处理-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/工作质量整改联络单处理-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/运维问题管理/(153-162)-工作质量整改联络单处理-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/配网电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(192-193)-配网电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/其它电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(194)-其它电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/其它电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(195)-其它电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/配网电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(196)-配网电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/其它电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(197)-其它电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/配网电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(198-199)-配网电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/台区变压器信息更新（公变台账同步）-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(200-202)-台区变压器信息更新（公变台账同步）-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/配网电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(203)-配网电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/其它电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(204)-其它电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/拓扑关系更新-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交拓扑关系更新/(207-208)-拓扑关系更新-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/线路信息更新（线路台账同步）-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(209-211)-线路信息更新（线路台账同步）-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/配网电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(212-217)-配网电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/其它电子化移交-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交台帐信息更新/(218)-其它电子化移交-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/低压单相（三相）新装、增减容-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(219-227)-低压单相（三相）新装、增减容-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/高压新装、增减容-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(228-237)-高压新装、增减容-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/零散居民新装-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(238-240)-零散居民新装-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/批量新装-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(241-243)-批量新装-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/直驳用电-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(244-246)-直驳用电-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/非永久性减容-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(247-249)-非永久性减容-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/减容恢复-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(250-252)-减容恢复-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/暂停-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(253-255)-暂停-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/暂停恢复-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(256-258)-暂停恢复-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/暂换及暂换恢复-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(259-261)-暂换及暂换恢复-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/暂拆-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(262-264)-暂拆-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/暂拆恢复-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(265-267)-暂拆恢复-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/更名-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(268-270)-更名-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/过户-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(271-273)-过户-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/销户-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(274-276)-销户-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/改类-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(277-279)-改类-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/受电装置变更-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(280-282)-受电装置变更-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/大客户新装、增容-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(283-299)-大客户新装、增容-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/高压新装、增减容-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(301-308)-高压新装、增减容-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/低压单相（三相）新装、增减容-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(309-315)-低压单相（三相）新装、增减容-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/零散居民新装-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/生产-营销/配网电子化移交单据/(316-321)-零散居民新装-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/营销业务对账流程-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/营销财务对账/(322-326)-营销业务对账流程-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/坏账核销处理-协同场景操作手册v.docx', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/坏账核销处理/(330-331)-坏账核销处理-协同场景操作手册v.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/提交购售电预算控制方案数据-协同场景操作手册.docx', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/提交购售电预算控制方案数据/(332)-提交购售电预算控制方案数据-协同场景操作手册.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步电厂结算单元-协同场景操作手册V1.0.doc', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/电价数据（购售电）/(335)-同步网间结算单元-协同场景操作手册V1.0.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步网间结算单元-协同场景操作手册V1.0.doc', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/电价数据（购售电）/(336)-同步网间结算单元-协同场景操作手册V1.0.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步电力用户应收电费核算单-协同场景操作手册V1.0.doc', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/电价数据（购售电）/(337)-同步电力用户应收电费核算单-协同场景操作手册V1.0.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步电厂购电结算通知单-协同场景操作手册V1.0.doc', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/电价数据（购售电）/(339)-同步电厂购电结算通知单-协同场景操作手册V1.0.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/同步网间购电结算通知单-协同场景操作手册V1.0.doc', 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/电价数据（购售电）/(340)-同步网间购电结算通知单-协同场景操作手册V1.0.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/营销管理系统与财务管理系统应用集成用户操作手册V2.2--支付退费确认.docx',
                 'C:/Users/tlju/Desktop/230场景操作手册/财务-营销/支付退费确认/(348-350)-营销管理系统与财务管理系统应用集成用户操作手册V2.2--支付退费确认.docx'],
                ['C:/Users/tlju/Desktop/所有操作手册/网络培训与评价系统与财务管理系统应用集成用户操作手册V2.1--教培费支付0320.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/财务-培评/教培费支付/(352-353)-网络培训与评价系统与财务管理系统应用集成用户操作手册V2.1--教培费支付0320.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-4A（同步功能服务）.doc', 'C:/Users/tlju/Desktop/230场景操作手册/人资-4A/同步用户与角色/(355)-协同场景操作手册-人资-4A（同步功能服务）.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-4A（同步角色服务）.doc', 'C:/Users/tlju/Desktop/230场景操作手册/人资-4A/同步用户与角色/(356)-协同场景操作手册-人资-4A（同步角色服务）.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-4A（同步角色与功能关系服务）.doc', 'C:/Users/tlju/Desktop/230场景操作手册/人资-4A/同步用户与角色/(357)-协同场景操作手册-人资-4A（同步角色与功能关系服务）.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-4A（同步用户与角色关系服务）.doc', 'C:/Users/tlju/Desktop/230场景操作手册/人资-4A/同步用户与角色/(359)-协同场景操作手册-人资-4A（同步用户与角色关系服务）.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-4A（同步账号服务）.doc', 'C:/Users/tlju/Desktop/230场景操作手册/人资-4A/同步用户与角色/(360)-协同场景操作手册-人资-4A（同步账号服务）.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-主数据（同步员工信息（新增、修改、删除））.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/人资-主数据/同步员工信息/(361-363)-协同场景操作手册-人资-主数据（同步员工信息（新增、修改、删除））.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-主数据（同步组织机构（新增、修改、删除））.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/人资-主数据/同步组织机构/(364-366)-协同场景操作手册-人资-主数据（同步组织机构（新增、修改、删除））.doc'],
                ['C:/Users/tlju/Desktop/所有操作手册/协同场景操作手册-人资-主数据（同步岗位信息（新增、修改、删除））.doc',
                 'C:/Users/tlju/Desktop/230场景操作手册/人资-主数据/同步岗位信息/(367-369)-协同场景操作手册-人资-主数据（同步岗位信息（新增、修改、删除））.doc']]
    for i in all_file:
        a = file_copy(i[0], i[1])
        if a:
            print('ok')
        else:
            print('error' + str(i))
