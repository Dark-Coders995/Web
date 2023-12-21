<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
      <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
        <li class="nav-item active">
        </li>
        <li class="nav-item">
          <router-link to="/bookings" class="btn btn-outline-danger" role="button">Bookings</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/search" class="btn btn-outline-danger" role="button">Search</router-link>
        </li>
        <li class="nav-item">
          <a class="btn btn-outline-danger" @click="logout" role="button">Logout</a>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
        <a class="navbar-brand" href="/userdash">Dashboard</a>
      </form>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'UserNav',
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/Login');
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
  margin-left: 70px;
}

.nav-link {
  color: #f8f3f7;
  text-decoration: wavy;
}
</style>
