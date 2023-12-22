<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
            <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
              <li class="nav-item">
                <a class="btn btn-outline-danger" href="http://localhost:5173/adminsignup" role="button">Admin Zone</a>
              </li>
            </ul> 
          </div>
        </nav>
    <div class="user-login">
        <form class="loginuser" @submit.prevent="Userlogin">
        <h1 class="login-page"> User Login</h1>
        <div class="login-form">
          <input type="text" placeholder="Enter Username" v-model="username" />
          <input type="password" placeholder="Enter Password" v-model="password" />
            <div class="button-container">
                <button @click.prevent="Userlogin">Login</button>
            </div>
        <div class="links-container">
            <div class="left-link">
                <a href="http://localhost:5173/sign-up">New User?</a>
            </div>
        </div>     
    </div>
  </form>
    </div>
</template>
<script>
import axios from "axios";
import LoginNav from './LoginNav.vue';

export default {
  name: "Login",
  components: {
    LoginNav
  },
    data() {
        return {
            username: "",
            password: "",
        };
    },
    methods: {
      Userlogin() {
        if (!this.username || !this.password) {
          alert("Please enter both the username and the password !!");
          return;
        }
        
        const userData = {
          username: this.username,
          password: this.password,
        };
        
        axios
          .post("http://127.0.0.1:5000/api/login", userData)
          .then((response) => {
            if (response.data.status === "success") {

              localStorage.setItem("access_token", response.data.access_token);
              alert("Successfully Logged in !!");
              this.$router.push("/userdash");
            } else {
              alert("Invalid credentials !!");
            }
          })
          .catch((error) => {
            console.error(error);
            if (error.response && error.response.data) {
              alert(error.response.data.error_message);
            } else {
              alert("An error occurred while logging in !!");
            }
          });
      },
    },

};
</script>

<style>
.logo{
  width: 60px;
  height: 60px;
  margin-top: 10px;
  position: fixed;
}
.loginuser {
  position: fixed;
  top: 53%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 400px;
  padding: 20px;
  background-color: #ddaeae;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.login-page {
  font-size: 24px;
  margin-top: 20px;
  font-weight: 400;
}
.user-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 80vh;
  padding-top: 20px;
  box-sizing: border-box;
}
.links-container {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  text-decoration: wavy;
  color: black;
}
.links-container a {
  text-decoration: wavy;
  color: black;
}
.login-form input {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
}
.login-form button {
    align-self: center;
    width: 200px;
    height: 40px;
    border: blue;
    color: gainsboro;
    background-color: black;
    cursor: pointer;
}
.button-container {
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>