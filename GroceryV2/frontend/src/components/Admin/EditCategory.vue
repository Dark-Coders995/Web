<template>
  <div v-if="isAuthenticated">
    <AdminNav />
    <br />
    <div class="category-edit">
      <h2>Edit Category</h2>
      <form @submit.prevent="savecategory">
        <div class="editcategory-form">
          <label for="category">Category</label>
          <input v-model="updatedCategory.name" type="text" placeholder="Name" />
          <label for="location">Description</label>
          <input v-model="updatedCategory.description" type="text" placeholder="Description" />
          <div class="button-container">
            <button type="submit">Save</button>
          </div>
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
import AdminNav from "./AdminNav.vue";

export default {
  name: "EditCategory",
  components: {
    AdminNav,
  },
  props: ['category'],
  data() {
    return {
      isAuthenticated: false,
      updatedCategory: {
        id: null,
        name: "",
        description: "",
      },
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.updatedcategory = { ...this.category };
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    savecategory() {
      const catId = this.$route.params.category_id;
      axios.put(`http://127.0.0.1:5000/api/admin/category/${catId}`, this.updatedCategory, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
      .then((response) => {
        console.log(response.data);
        window.alert("Category updated successfully");
        this.$router.push("/admindash");
      })
      .catch((error) => {
        console.error(error);
        window.alert("Failed to update category");
      });
    },
  }
};
</script>

<style>
.category-edit {
  position: fixed;
  top: 50%;
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

.editcategory-form input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid black;
}

.editcategory-form button {
  align-self: center;
  width: 200px;
  height: 40px;
  border: none;
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
