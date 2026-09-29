<script>
import axios from 'axios'
export default{
    data(){
        return {
            formData:{
                username : "", 
                password : "",
                email : ""
            },
            error : false
        }
    },

    methods : {
        async registerUser(){
          try{
            const resp = await axios.post('http://127.0.0.1:5000/api/register',this.formData, {
                'Content-Type' : 'application/json',
            }) 
            if(resp.status==201){
              this.error = false
              console.log("success")
              this.$router.push('/login')
            }  
          }catch(error){
            this.error = error.response.data.error
          }
      }
  }
}
</script>

<template>
  <div class="register-container">
    <form class="register-form" @submit.prevent="registerUser">
      <h2>Register</h2>

      <div class="form-group">
        <label for="username">Username</label>
        <input
          id="username"
          type="text"
          v-model="formData.username"
          placeholder="Enter username"
          required
        />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          type="email"
          v-model="formData.email"
          placeholder="Enter email"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          type="password"
          v-model="formData.password"
          placeholder="Enter password"
          required
        />
      </div>

      <p v-if="error" id="error">{{ error }}</p>

      <button type="submit">Register</button>

      <div class="form-group">
        <p style="text-align : center">
          Already have an account?
          <router-link to="/login">Login</router-link>
        </p>
      </div>

    </form>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
}

#error {
  text-align: center;
  color: red;
}

.register-form {
  width: 350px;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.register-form h2 {
  text-align: center;
  margin-bottom: 25px;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: #42b883;
}

.register-form button {
  width: 100%;
  padding: 11px;
  border: none;
  border-radius: 6px;
  background: #42b883;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.register-form button:hover {
  background: #369f6e;
}
</style>