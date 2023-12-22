<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
      <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
        <li class="nav-item">
          <a class="btn btn-outline-danger" href="http://localhost:5173/sign-up" role="button">User Zone</a>
        </li>
      </ul> 
    </div>
  </nav>
    <div class="admin-login">
        <form class="loginadmin" @submit.prevent="Adminlogin">
        <h1 class="adminlogin-page"> Admin Login</h1>
        <div class="adminlogin-form">
          <input type="text" placeholder="Enter Username" v-model="username" />
          <input type="password" placeholder="Enter Password" v-model="password" />
            <div class="button-container">
                <button @click.prevent="Adminlogin">Login</button>
            </div>
            <div class="links-container">
            <div class="left-link">
                <a href="http://localhost:5173/adminsignup">New Admin?</a>
            </div>
        </div>  
        </div>
        </form>
    </div>
</template>
<script>
import axios from "axios";

export default {
    name: "AdminLogin",
    data() {
        return {
            username: "",
            password: "",
        };
    },
    methods: {
      Adminlogin() {
        if (!this.username || !this.password) {
          alert("Please enter both the username and the password !!");
          return;
        }
        
        const userData = {
          username: this.username,
          password: this.password,
        };
        
      axios
        .post("http://127.0.0.1:5000/api/admin/login", userData)
        .then((response) => {
          if (response.data.status === "success") {
            localStorage.setItem("access_token", response.data.access_token);

            alert("Successfully Logged in !!");
            this.$router.push("/admindash");
          } 
          else {
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
.loginadmin {
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
.adminlogin-page {
  font-size: 24px;
  margin-top: 20px;
  font-weight: 400;
}
.admin-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 80vh;
  padding-top: 20px;
  box-sizing: border-box;
}

.adminlogin-form input {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
}
.adminlogin-form button {
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