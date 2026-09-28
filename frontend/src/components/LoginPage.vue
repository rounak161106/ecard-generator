<script>
import axios from 'axios'
export default{
    data(){
        return {
            formData:{
                username : "", 
                password : ""
            },
            token : "",
            error : false
        }
    },

    methods : {
        async loginUser(){
          try{
            const resp = await axios.post('http://127.0.0.1:5000/api/login',this.formData, {
                'Content-Type' : 'application/json',
            }) 
            if(resp.status==200){
              this.error=false
              localStorage.setItem("token" , resp.data.access_token)
              this.token = resp.data.access_token
              console.log("added")
              console.log(this.error)
            }  
          }catch(error){
              this.error = true
              console.log("Invalid Credentials")
              console.log(this.error)
        }
      }
  }
}
</script>

<template>
  <div class="login-container">
    <form class="login-form" @submit.prevent="login">
      <h2>Login</h2>

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
        <label for="password">Password</label>
        <input
          id="password"
          type="password"
          v-model="formData.password"
          placeholder="Enter password"
          required
        />
      </div>

      <p v-if="error" id="error">Invalid Credentials</p>

      <button @click="loginUser" type="submit">Login</button>

      <div class="form-group">
        <p style="text-align : center">Are you a new user? <a href="#">Register</a> </p>
      </div>

    </form>
  </div>
</template>

<style scoped>
    .login-container {
    min-height: 80vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f5f5f5;
    }
    
    #error{
      text-align : center;
      color : red
    }

    .login-form {
    width: 350px;
    padding: 30px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .login-form h2 {
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

    .login-form button {
    width: 100%;
    padding: 11px;
    border: none;
    border-radius: 6px;
    background: #42b883;
    color: white;
    font-size: 16px;
    cursor: pointer;
    }

    .login-form button:hover {
    background: #369f6e;
    }
</style>