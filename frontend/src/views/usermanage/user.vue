<template>
    <div class="app-container">
        <div class="filter-container">
            <el-select v-model="listQuery.type" placeholder="Type" clearable class="filter-item" style="width: 130px">
                <el-option v-for="item in searchTypeOptions" :key="item.key"
                           :label="item.display_name" :value="item.key"/>
            </el-select>
            <el-input v-model="listQuery.title" placeholder="输入关键字搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter"
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
            <el-table-column label="用户名" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.username }}</span>
                </template>
            </el-table-column>
            <el-table-column label="部门" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.department }}</span>
                </template>
            </el-table-column>
            <el-table-column label="手机" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.tel }}</span>
                </template>
            </el-table-column>
            <el-table-column label="邮箱" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.email }}</span>
                </template>
            </el-table-column>
            <el-table-column label="状态" align="center">
                <template slot-scope="scope">
                    <el-switch v-model="scope.row.is_active"
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
            <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px"
                     style="width: 400px; margin-left:50px;">
                <el-form-item label="部门" prop="department">
                    <el-select v-model="temp.department" class="filter-item" placeholder="Please select">
                        <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name"
                                   :value="item.key"/>
                    </el-select>
                </el-form-item>
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="temp.username"/>
                </el-form-item>
                <el-form-item label="电话" prop="tel">
                    <el-input v-model="temp.tel"/>
                </el-form-item>
                <el-form-item label="状态" prop="is_active">
                    <el-select v-model="temp.is_active" class="filter-item" placeholder="Please select">
                        <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item"/>
                    </el-select>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="temp.email"/>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="temp.password" placeholder="请输入密码" minlength="6" show-password/>
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
    import {getuserlist, createUser, delUser, updateUser} from '@/api/user'
    import waves from '@/directive/waves' // waves directive
    import {parseTime} from '@/utils'
    import Pagination from '@/components/Pagination' // secondary package based on el-pagination

    const calendarTypeOptions = [
        {key: '运维', display_name: '运维部'},
        {key: '测试', display_name: '测试部'},
        {key: 'UI', display_name: 'UI部'},
        {key: '开发', display_name: '开发部'}
    ]
    const searchTypeOptions = [
        {key: 'username', display_name: '用户名'},
        {key: 'department', display_name: '部门'}
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
                calendarTypeOptions,
                searchTypeOptions,
                //dialog 状态选择框
                statusOptions: ['激活', '锁定'],
                temp: {
                    // id: undefined,
                    username: '',
                    department: '',
                    tel: '',
                    email: '',
                    roles: [2],
                    is_active: '激活',
                    password: '123456'
                },
                dialogFormVisible: false,
                dialogStatus: '',
                //复用时的动态title
                textMap: {
                    update: '更新用户',
                    create: '创建用户'
                },
                //dialog里表单字段验证规则
                rules: {
                    username: [{required: true, message: 'username is required', trigger: 'blur'}],
                    department: [{required: true, message: 'department is required', trigger: 'change'}],
                    email: [{type: 'email', required: true, message: 'email is required', trigger: 'blur'}],
                    password: [{required: true, message: 'password is required', trigger: 'blur'}]
                },
            }
        },
        created() {
            this.getList()
        },
        methods: {
            getList() {
                this.listLoading = true
                getuserlist(this.listQuery).then(response => {
                    this.list = response.data
                    this.total = response.count
                    this.listLoading = false

                })
            },
            handleFilter() {
                this.listQuery.page = 1
                this.getList()
            },
            resetTemp() {
                this.temp = {
                    // id: undefined,
                    username: '',
                    department: '',
                    tel: '',
                    email: '',
                    roles: [2],
                    is_active: '激活',
                    password: '123456'
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
                        createUser(this.temp).then((res) => {
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
                delUser({user_id: row.id}).then(() => {
                    this.$message({
                        message: '操作Success',
                        type: 'success',
                        duration: 2000
                    })
                    const index = this.list.indexOf(row)
                    this.list.splice(index, 1)
                })

            },
            updateData() {
                this.$refs['dataForm'].validate((valid) => {
                    if (valid) {
                        const tempData = Object.assign({}, this.temp)
                        updateUser(tempData).then((res) => {
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
