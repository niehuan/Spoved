<template>
    <div class="app-container">
        <div class="filter-container">
            <el-select v-model="listQuery.type" placeholder="Type" clearable class="filter-item" style="width: 130px">
                <el-option v-for="item in searchTypeOptions" :key="item.key"
                           :label="item.display_name" :value="item.key"/>
            </el-select>
            <el-input v-model="listQuery.title" placeholder="输入关键字搜索" style="width: 200px;" class="filter-item"
                      @keyup.enter.native="handleFilter"
            />
            <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
                搜索
            </el-button>
            <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit"
                       @click="handleCreate">
                新增
            </el-button>
        </div>
        <el-table
                :key="tableKey"
                v-loading="listLoading"
                :data="list"
                border
                fit
                highlight-current-row
                style="width: 100%">
            <!--<el-table-column prop="id" label="ID" align="center">-->
            <!--<template slot-scope="scope">-->
            <!--<span>{{ scope.row.id }}</span>-->
            <!--</template>-->
            <!--</el-table-column>-->
            <el-table-column label="权限名称" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.name }}</span>
                </template>
            </el-table-column>
            <el-table-column label="请求方法" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.method_type }}</span>
                </template>
            </el-table-column>
            <el-table-column label="请求路径" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.url }}</span>
                </template>
            </el-table-column>
            <el-table-column label="状态" align="center">
                <template slot-scope="scope">
                    <el-switch v-model="scope.row.status==='0'"
                               active-color="#13ce66"
                               inactive-color="#ff4949"
                               disabled>
                    </el-switch>
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                <template slot-scope="{row}">
                    <el-button type="primary" size="mini" @click="handleUpdate(row)">
                        更新
                    </el-button>
                    <el-button type="danger" size="mini" @click="deleteData(row)">
                        删除
                    </el-button>
                </template>
            </el-table-column>

        </el-table>
        <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit"
                    @pagination="getList"/>

        <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
            <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="80px"
                     style="width: 400px; margin-left:50px;">
                <el-form-item label="请求方法" prop="method_type">
                    <el-select v-model="temp.method_type" class="filter-item" placeholder="Please select">
                        <el-option v-for="item in methodTypeOptions" :key="item.key" :label="item.display_name"
                                   :value="item.key"/>
                    </el-select>
                </el-form-item>
                <el-form-item label="权限名称" prop="name">
                    <el-input v-model="temp.name"/>
                </el-form-item>
                <el-form-item label="请求路径" prop="url">
                    <el-input v-model="temp.url"/>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">
                    取消
                </el-button>
                <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
                    确定
                </el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import {getFuncslist, createFunc, delFunc, updateFunc} from '@/api/user'
    import waves from '@/directive/waves' // waves directive
    import {parseTime} from '@/utils'
    import Pagination from '@/components/Pagination' // secondary package based on el-pagination

    const methodTypeOptions = [
        {key: 'GET', display_name: 'GET'},
        {key: 'POST', display_name: 'POST'},
        {key: 'PUT', display_name: 'PUT'},
        {key: 'DELETE', display_name: 'DELETE'},
        {key: 'PATCH', display_name: 'PATCH'},
        {key: 'ALL', display_name: 'ALL'}
    ]
    const searchTypeOptions = [
        {key: 'name', display_name: '权限名称'},
        {key: 'url', display_name: '请求路径'},
        {key: 'method_type', display_name: '请求方法'}
    ]
    export default {
        name: 'user',
        components: {Pagination},
        directives: {waves},
        filters: {},
        data() {
            return {
                tableKey: 0,
                list: null,
                total: 0,
                listLoading: true,
                listQuery: {
                    page: 1,
                    limit: 20,
                    title: undefined,
                    type: undefined,
                    sort: '+id'
                },
                methodTypeOptions,
                searchTypeOptions,
                //dialog 状态选择框
                // statusOptions: ['激活', '锁定'],
                temp: {
                    // id: undefined,
                    name: '',
                    method_type: '',
                    url: ''
                },
                dialogFormVisible: false,
                dialogStatus: '',
                //复用时的动态title
                textMap: {
                    update: '更新权限',
                    create: '新建权限'
                },
                //dialog里表单字段验证规则
                rules: {
                    name: [{required: true, message: '权限名称不能为空', trigger: 'blur'}],
                    url: [{required: true, message: '请求路径不能为空', trigger: 'blur'}],
                    method_type: [{required: true, message: '请求方法不能为空', trigger: 'change'}],
                },
            }
        },
        created() {
            this.getList()
        },
        methods: {
            getList() {
                this.listLoading = true
                getFuncslist(this.listQuery).then(response => {
                    this.list = response.data
                    this.total = response.count

                    // Just to simulate the time of the request
                    setTimeout(() => {
                        this.listLoading = false
                    }, 1.5 * 1000)
                })
            },
            handleFilter() {
                this.listQuery.page = 1
                this.getList()
            },
            resetTemp() {
                this.temp = {
                    // id: undefined,
                    name: '',
                    method_type: '',
                    url: ''
                }
            },
            handleCreate() {
                this.resetTemp()
                this.dialogStatus = 'create'
                this.dialogFormVisible = true
                //this.$nextTick()当数据被修改后使用这个方法会回调获取更新后的dom再render出来
                this.$nextTick(() => {
                    this.$refs['dataForm'].clearValidate()
                })
            },
            handleUpdate(row) {
                this.temp = Object.assign({}, row) //es6 深拷贝
                this.dialogStatus = 'update'
                this.dialogFormVisible = true
                this.nextTick(() => {
                    this.$refs['dataForm'].clearValidate()
                })

            },
            createData() {
                this.$refs['dataForm'].validate((valid) => {
                    if (valid) {
                        // this.temp.id = parseInt(Math.random() * 100)
                        createFunc(this.temp).then((res) => {
                            this.list.push(res.data)
                            this.dialogFormVisible = false
                            this.$notify({
                                title: 'Success',
                                message: '创建成功',
                                type: 'success',
                                duration: 3000
                            })
                        })
                    }
                })
            },
            deleteData(row) {
                this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    delFunc({func_id: row.id}).then(() => {
                    this.$message({
                        message: '操作Success',
                        type: 'success',
                        duration: 2000
                    })
                    const index = this.list.indexOf(row)
                    this.list.splice(index, 1)
                })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });


            },
            updateData() {
                this.$refs['dataForm'].validate((valid) => {
                    if (valid) {
                        const tempData = Object.assign({}, this.temp)
                        updateFunc(tempData).then((res) => {
                            for (const v of this.list) {
                                if (v.id === res.data.id) {
                                    const index = this.list.indexOf(v)
                                    this.list.splice(index, 1, res.data)
                                    break
                                }
                            }
                            this.dialogFormVisible = false
                            this.$notify({
                                title: 'Success',
                                message: '更新成功',
                                type: 'success',
                                duration: 2000
                            })
                        })
                    }
                })
            }

        }
    }
</script>
