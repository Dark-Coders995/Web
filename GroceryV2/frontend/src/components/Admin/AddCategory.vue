<template>
  <div v-if="isAuthenticated">
    <AdminNav />
    <br />
    <div class="categoryadd">
      <h2>Creating A New Category</h2>
      <form class="addcategory-form" @submit.prevent="createcategory">
        <div class="form-group">
          <label for="category">Name</label>
          <input type="text" v-model="name" class="form-control" placeholder="Name" required />
        </div>
        <div class="form-group">
          <label for="Place">Decription</label>
          <input type="text" v-model="place" class="form-control" placeholder="Place" required />
        </div>
        <div class="button-container">
          <button type="submit" class="btn btn-primary" @click.prevent="createcategory">
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
    <div v-else>
      <h1>You need to log in as an admin to access this page.</h1>
    </div>
</template>

<script>
import axios from "axios";
import AdminNav from './AdminNav.vue'

export default {
  name: "AddCategory",
  components: {
    AdminNav
  },
  data() {
    return {
      isAuthenticated: false,
      name: "",
      description: ""
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
    }
  },
  methods: {
    createcategory() {
      const CategoryData = {
        name: this.name,
        description: this.description
      };

      axios.post("http://127.0.0.1:5000/api/admin/category", CategoryData, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
      .then(response => {
        console.log(response.data);
        alert("category Added Successfully");
        this.$router.push("/admindash");
      })
      .catch(error => {
        console.error(error);
        alert("Can't Add Category! Try Again");
      });
    }
  }
};
</script>



  <style>
  .categoryadd {
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
  
  .addcategory-form input {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
  }
  
  .addcategory-form button {
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