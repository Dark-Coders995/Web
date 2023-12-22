<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
      <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
        <li class="nav-item">
          <button class="btn btn-outline-danger" @click="logout" role="button">Logout</button>
        </li>
        <li class="nav-item">
          <router-link to="/summary" class="btn btn-outline-danger" role="button">Summary</router-link>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
        <a class="navbar-brand" href="/admindash">Dashboard</a>
      </form>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNav',
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push({ name: 'AdminLogin' });
      window.alert('You are logged out.');
    }
  }
};
</script>
  
  <style>
  .navbar {
    background-color: #000;
    color: #fff;
    padding: 10px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 999;
  }
  
  .navbar-brand {
    font-weight: bold;
    font-size: 20px;
  }
  
  .navbar-nav {
    display: flex;
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  
  .nav-item {
    margin-left: 10px;
  }
  
  .nav-link {
    color: #fff;
    text-decoration: none;
  }
  </style>

  
    