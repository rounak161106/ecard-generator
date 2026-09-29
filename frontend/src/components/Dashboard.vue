<template>
    <div v-if="token">
        <div v-if="role=='user'">
            <h2>Welcome {{ userData.username }} !!</h2>
            <h3>Your cards</h3>
            <table border="" cellpadding="5px">
                <thead>
                    <tr>
                        <th>Card Name</th>
                        <th>key</th>
                        <th colspan="2">Action </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="card in userData.card_requests">
                        <td>{{ card.cardname }}</td>
                        <td>{{ }}</td>
                        <td>View</td>
                        <td>Delete</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <h2>Welcome {{ userData.admin_name }} !!</h2>
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
                    this.userData = resp.data
                    this.role = resp.data.role
                    console.log(this.userData)
                    console.log(resp)
                    console.log(this.userData.card_request_details)
                    }  
                }catch(error){
                    console.log(error)
                }
            },
        }
    }
</script>