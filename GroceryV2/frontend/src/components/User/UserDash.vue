<template>
  <div class="background-image" v-if="isAuthenticated && isUser">
    <UserNav v-if="isUser" />
    <div class="container mt-4 category-container">
      <div class="row">
        <div
          v-for="category in categories"
          :key="category.id"
          class="col-md-6 mb-4">
          <div class="category-card">
            <h3 class="location-text">{{ category.name }}</h3>
            <h6 class="location-text">{{ category.description }}</h6>
            <button @click="redirectToProducts(category.id)">Get Products</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <h1>You need to log in as a user to access this page.</h1>
  </div>
</template>

<script>
import axios from "axios";
import UserNav from './UserNav.vue';

export default {
  name: 'UserDash',
  components: {
    UserNav
  },
  data() {
    return {
      categories: [],
      isUser: false
    };
  },
  computed: {
    isAuthenticated() {
      const token = localStorage.getItem('access_token');
      return !!token; 
    }
  },
  mounted() {
    if (this.isAuthenticated) {
      this.fetchCategories();
    }
  },
  methods: {
    fetchCategories() {
      const token = localStorage.getItem('access_token');
      axios.get('http://127.0.0.1:5000/api/user/categories', {
        headers: { 'Authorization': 'Bearer ' + token }
      })
        .then(response => {
          this.categories = response.data;
          this.isUser=true;
        })
        .catch(error => {
          console.error(error);
          this.isUser=false;
        });
    },
    redirectToProducts(category_id) {
      this.$router.push({ name: 'Products', params: { category_id: category_id } });
    }
  }
};
</script>

<style>

 body {
  background-size: cover; 
  background-repeat: no-repeat; 
  min-height: 100vh; 
}

.category-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; 
}
  .category-card {
  width: 220px; 
  background-color: #9c8e8e; 
  color: #0a0000; 
  padding: 20px;
  margin: 10px; 
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .location-text {
    margin-top: auto;
    margin-bottom: 10px;
    text-align: center;
  }

  .category-card button {
    cursor: pointer;
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 50px;
    border-radius: 5px;
    transition: background-color 0.3s;
    
  }

  button:hover {
    background-color: #0056b3;
  }

  .user-nav {
    position: sticky;
    top: 0;
    background-color: #f9f9f9; 
    z-index: 999;
  }

  .category-container {
    max-height: calc(100vh - 60px); 
    overflow-y: auto;
  }

</style>
