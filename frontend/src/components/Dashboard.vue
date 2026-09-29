<template>
    <div v-if="token">
        <div v-if="role=='user'">
            <p>Welcome {{ userData.username }} !!</p>
        </div>
        <div v-else>
            <h2>Welcome {{ userData.admin_name }} !!</h2>
            <table border="2">
                <th></th>
            </table>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        data(){
            return {
                token : "",
                role : "",
                userData : ""
            }
        },
        mounted : function(){
            this.loadToken()
            this.loadData()
        },
        methods : {
            loadToken(){
                const token = localStorage.getItem("token")
                if(token){
                    this.token = token
                }else{
                    this.$router.push('/login')
                }
            },
            async loadData(){
                try{
                    const resp = await axios.get('http://127.0.0.1:5000/api/dashboard', {
                        headers : {
                            "Content-Type" : "application/json",
                            "Authorization" : `Bearer ${this.token}`
                        }
                    }) 
                    if(resp.status==200){
                    console.log(resp)
                    this.userData = resp.data
                    this.role = resp.data.role
                    }  
                }catch(error){
                    console.log(error)
                }
            },
        }
    }
</script>