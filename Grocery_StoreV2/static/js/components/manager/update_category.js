const ManagerPage2= Vue.component("update_category",{

    data: function () {
    return {
      errorMessage: "",
      category_name: "",
      error_1: false
    }
  },
    template:`
    <div class="login-card">
    <h2 class="text-center mb-4">Edit category</h2>
    <form @submit.prevent="editCategory">
      <div class="form-group">
        <label for="category_name"> New Category Name</label>
        <input v-model="category_name" class="form-control" id="category_name" name="category_name" required type="text">
      </div>
      <button class="btn btn-primary w-100" type="submit">Edit Category</button>
    </form>
  </div>
    `,

    methods:{
        editCategory(){
             this.error = "";
            const category_id = this.$route.params.category_id;
             const url =`/api/manager/update_category/${category_id}`
            console.log(url)

            fetch(url, {
                method: 'PUT',
                headers: {
                   // 'x-access-tokens': localStorage.getItem('auth_token')
                       'Content-Type': 'application/json'
                },
                body: JSON.stringify({category_name : this.category_name})
            })
                .then(response => {
                    if (response.ok) {
                         this.$router.push('/manager_logged');
                    } else {
                        this.error = data["error_message"]
                        if (data["error_code"] == "BE1001") {
                            this.error_1 = true
                            this.$refs.category_name.focus();
                        }
                    }
                });
        },
    }
});

export default ManagerPage2;