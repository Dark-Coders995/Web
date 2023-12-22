const ManagerPage3 = Vue.component("add_category",{

    data: function () {
    return {
      errorMessage: "",
      category_name: "",
      error_1: false
    }
  },

    template: `
        <div class="login-card">
            <h2 class="text-center mb-4">Add Category</h2>
            <form @submit.prevent="AddCategory">
                <div class="form-group">
                    <label for="category_name">Category Name </label>
                    <input v-model="category_name" ref="category_name"  v-bind:class="[error_1 ? 'category_name' : '', 'form-control']" type="text" class="form-control" id="category_name" placeholder="Enter Category Name" >
                </div>
                <button  class="btn btn-primary w-100" type="submit">Add Category</button>
            </form>
        </div>
    `,
    methods: {
        AddCategory: function (event) {
            this.error = "";
            var url = "/api/manager/add_category";
            console.log(url);

            fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({category_name: this.category_name})
            }).then(response => {
                if (!response.ok) {
                    response.json().then(data => {
                        this.error = data["error_message"]
                        if (data["error_code"] == "BE1001") {
                            this.error_2 = true
                            this.category_name = ""
                            this.$refs.category_name.focus();
                        }
                    })
                }
                else if (response.ok) {
                   //response.json().then(data =>
                     //  localStorage.setItem('auth_token', data['token']));
                   this.$router.push('/manager_logged');
                }
            })
        },
    }
});

export default ManagerPage3;
