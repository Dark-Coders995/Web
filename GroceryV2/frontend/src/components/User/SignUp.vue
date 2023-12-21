<template>
  <div>
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
    <div class="user-signup">
      <form class="signup" @submit.prevent="registerUser">
        <h1 class="signup-page">User SignUp</h1>
        <div class="signup-form">
          <input v-model="username" type="text" placeholder="Enter Username" />
          <input v-model="email" type="text" placeholder="Enter Email" />
          <input v-model="password" type="password" placeholder="Enter Password" />
          <div v-if="alertMessage" class="alert alert-danger">
            {{ alertMessage }}
          </div>
          <div class="button-container">
            <button type="submit">Register Now</button>
          </div>
          <div class="links-container">
            <div class="left-link">
              <a href="http://localhost:5173/Login">Registered User?</a>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      alertMessage: '' // New data property for alert messages
    };
  },
  methods: {
    registerUser() {
      this.alertMessage = ''; // Clear previous alert message

      if (!this.username || !this.email || !this.password) {
        this.alertMessage = "All fields are required !!";
        return;
      }

      if (!this.email.includes("@") || !this.email.endsWith(".com")) {
        this.alertMessage = "Invalid email format !! Email must include '@' and end with '.com'";
        return;
      }

      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
      };

      axios.post("http://127.0.0.1:5000/api/signup", userData)
        .then((response) => {
          if (response.data.alert) {
            this.alertMessage = response.data.alert;
          } else {
            alert("Successfully Registered !!");
            this.$router.push("/Login");
          }
        })
        .catch((error) => {
          console.error(error);
          this.alertMessage = "An error occurred while registering the user";
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
.signup {
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
.signup-page {
  font-size: 24px;
  margin-top: 20px;
  font-weight: 400;
}
.user-signup {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 80vh;
  padding-top: 20px;
  box-sizing: border-box;
}
.signup-form input {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
}
.signup-form button {
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