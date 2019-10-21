<template>
    <div class="app-container">
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit"
                   @click="handleCreate">
            新增
        </el-button>

        <el-table
                :key="tableKey"
                v-loading="listLoading"
                :data="list"
                border
                fit
                highlight-current-row
                style="width: 100%">
            <el-table-column label="角色" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.name }}</span>
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
                <template slot-scope="scope">
                    <el-button type="primary" size="mini" @click="handleUser(scope)">
                        用户
                    </el-button>
                    <el-button type="primary" size="mini" @click="handleCpn(scope)">
                        组件
                    </el-button>
                    <el-button type="primary" size="mini" @click="handleMenu(scope)">
                        菜单
                    </el-button>
                    <el-button type="primary" size="mini" @click="handlePerms(scope)">
                        权限
                    </el-button>
                    <el-button type="danger" size="mini" @click="deleteData(scope)">
                        删除
                    </el-button>
                </template>
            </el-table-column>

        </el-table>
        <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit"
                    @pagination="getList"/>

        <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
            <el-form ref="dataForm" :model="temp" label-position="left" label-width="80px"
                     style="width: 400px; margin-left:50px;">
                <el-form-item :label="textMap[dialogStatus]">
                    <el-tree
                            ref="tree"
                            :check-strictly="checkStrictly"
                            :data="mixinData"
                            :props="defaultProps"
                            show-checkbox
                            node-key="id"
                            class="permission-tree"
                    />
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button type="danger" @click="dialogFormVisible = false">
                    取消
                </el-button>
                <el-button type="primary"
                           @click="dialogStatus==='user'?createUserData():dialogStatus==='cpn'?createCpnData():dialogStatus==='menu'?createMenuData():createPermsData()">
                    确定
                </el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import {
        createRoleMenu,
        getMenuAll,
        getUserAll,
        createRolePerms,
        createRoleUsers,
        getRoleFunc,
        getFuncAll,
        getRoleslist,
        createFunc,
        delFunc,
        updateFunc
    } from '@/api/user'
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
                //dialog 状态选择框
                methodTypeOptions,
                checkStrictly: false,
                total_data: [],
                temp: {
                    // id: undefined,
                    name: '',
                    currentPerm: [],
                    currentUser: undefined,
                    currentMenu: undefined
                },
                dialogFormVisible: false,
                dialogStatus: '',
                //复用时的动态title
                textMap: {
                    user: '用户',
                    cpn: '组件',
                    menu: '菜单',
                    perms: '权限',
                },
                defaultProps: {
                    children: '',
                    label: ''
                }
            }
        },
        computed: {
            mixinData() {
                return this.total_data
            },
        },
        created() {
            this.getList()
        },
        methods: {
            getList() {
                this.listLoading = true
                getRoleslist(this.listQuery).then(response => {
                    this.list = response.data
                    this.total = response.count
                    this.listLoading = false

                })
            },
            //获取全部权限
            async getAllperms() {
                this.defaultProps.label = 'name'
                const res = await getFuncAll({flag: 1})
                this.total_data = res.data
            },
            //获取所属角色权限,返回的是权限表id，如[1,3,5,6]。
            async getRoleperms(name) {
                const res = await getFuncAll({flag: 0, name: name})
                this.$nextTick(() => {
                    this.$refs.tree.setCheckedKeys(res.data)
                    this.temp.currentPerm = res.data
                    this.temp.name = name
                })
            },
            //获取全部用户
            async getAllusers() {
                this.defaultProps.label = 'username'
                // this.$refs.tree.setCheckedKeys([])
                const res = await getUserAll({flag: 1})
                this.total_data = res.data
            },
            //获取所属角色用户,返回的是用户表id，如[1,3,5,6]。
            async getRoleusers(name) {
                const res = await getUserAll({flag: 0, name: name})
                this.$nextTick(() => {
                    this.$refs.tree.setCheckedKeys(res.data)
                    this.temp.currentUser = res.data
                    this.temp.name = name
                })
            },
            //获取全部菜单
            async getAllmenu() {
                this.defaultProps.label = 'name'
                const res = await getMenuAll({flag: 1})
                this.total_data = res.data
            },
            //获取所属角色菜单
            async getRolemenu(name) {
                const res = await getMenuAll({flag: 0, name: name})
                this.$nextTick(() => {
                    this.$refs.tree.setCheckedKeys(res.data)
                    this.temp.currentMenu = res.data
                    this.temp.name = name
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
                    currentPerm: []
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
            //处理角色权限变更
            handlePerms(scope) {
                this.getAllperms()
                this.getRoleperms(scope.row.name)
                this.dialogStatus = 'perms'
                this.dialogFormVisible = true
                this.$nextTick(() => {
                    this.$refs['dataForm'].clearValidate()
                })
            },
            //处理角色用户变更
            handleUser(scope) {
                this.getAllusers()
                this.getRoleusers(scope.row.name)
                this.dialogStatus = 'user'
                this.dialogFormVisible = true
                this.$nextTick(() => {
                    this.$refs['dataForm'].clearValidate()
                })
            },
            //处理角色组件变更
            handleCpn(scope) {
                this.dialogStatus = 'cpn'
                this.dialogFormVisible = true
                this.$nextTick(() => {
                    this.$refs['dataForm'].clearValidate()
                })
            },
            //处理角色菜单变更
            handleMenu(scope) {
                this.getAllmenu()
                this.getRolemenu(scope.row.name)
                this.dialogStatus = 'menu'
                this.dialogFormVisible = true
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
            //添加修改该角色所拥有的用户
            createUserData() {
                const checkedKeys = this.$refs.tree.getCheckedKeys()
                const beforeChecked = this.temp.currentUser
                const roleNameChecked = this.temp.name
                createRoleUsers({
                    newRoleUsers: checkedKeys,
                    oldRoleUsers: beforeChecked,
                    name: roleNameChecked
                }).then(() => {
                    this.dialogFormVisible = false
                    this.$notify({
                        title: 'Success',
                        message: '修改成功',
                        type: 'success',
                        duration: 3000
                    })
                })
            },
            createCpnData() {
                console.log(2);
            },
            //添加修改该角色所拥有的菜单
            createMenuData() {
                const checkedKeys = this.$refs.tree.getCheckedKeys()
                const beforeChecked = this.temp.currentMenu
                const roleNameChecked = this.temp.name
                createRoleMenu({
                    newRoleMenu: checkedKeys,
                    oldRoleMenu: beforeChecked,
                    name: roleNameChecked
                }).then(() => {
                    this.dialogFormVisible = false
                    this.$notify({
                        title: 'Success',
                        message: '修改成功',
                        type: 'success',
                        duration: 3000
                    })
                })
            },
            //添加修改该角色所拥有的权限
            createPermsData() {
                const checkedKeys = this.$refs.tree.getCheckedKeys()
                const beforeChecked = this.temp.currentPerm
                const roleNameChecked = this.temp.name
                createRolePerms({
                    newRolePerms: checkedKeys,
                    oldRolePerms: beforeChecked,
                    name: roleNameChecked
                }).then(() => {
                    this.dialogFormVisible = false
                    this.$notify({
                        title: 'Success',
                        message: '修改成功',
                        type: 'success',
                        duration: 3000
                    })
                })
            },
            deleteData(row) {
                this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(async () => {
                    await delFunc({func_id: row.id})
                    const index = this.list.indexOf(row)
                    this.list.splice(index, 1)
                    this.$message({
                        message: '操作Success',
                        type: 'success',
                        duration: 2000
                    })

                }).catch(err => {
                    console.error(err)
                })


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

<style lang="scss" scoped>
    .app-container {
        .permission-tree {
            margin-bottom: 30px;
        }
    }
</style>