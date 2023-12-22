const Page2 = Vue.component("signup",{

    data: function () {
    return {
      errorMessage: "",
      email: "",
      user_name: "",
      password: "",
      error_1: false,
      error_2: false,
      error_3: false
    }
  },

    template: `
        <div class="login-card">
            <h2 class="text-center mb-4">User Sign Up</h2>
            <form @submit.prevent="signUp">
                <div class="form-group">
                    <label for="user_name">Username</label>
                    <input v-model="user_name" ref="user_name"  v-bind:class="[error_1 ? 'user_name' : '', 'form-control']" type="text" class="form-control" id="user_name" placeholder="Enter username" >
                </div>
                <div class="form-group">
                    <label for="email"">Email:</label>
                     <input v-model="email" ref="email" v-bind:class="[error_3 ? 'email' : '', 'form-control']" type="email" class="form-control" id="email" placeholder="Enter Email ID">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input v-model="password" ref="password" v-bind:class="[error_2 ? 'password' : '', 'form-control']" type="password" class="form-control" id="password" placeholder="Enter password" >
                </div>
                <button class="btn btn-primary w-100" type="submit">Sign Up</button>
            </form>
            <p class="mt-3">Already have an account? <router-link to="/">Login</router-link></p>
            <router-link to="/manager_login">Manager Login</router-link>
        </div>
    `,
    methods: {
        signUp: function (event) {
            this.error = "";
            var url = "/api/user/sign_up";
            console.log(url);

            fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user_name: this.user_name, email: this.email, password: this.password})
            }).then(response => {
                if (!response.ok) {
                    response.json().then(data => {
                        this.error = data["error_message"]
                        if (data["error_code"] == "BE104") {
                            this.error_3 = true
                            this.email = ""
                            this.$refs.email.focus();
                        } else if (data["error_code"] == "BE105") {
                            this.error_1 = true
                            this.user_name = ""
                            this.$refs.user_name.focus()
                        } else if (data["error_code"] == "BE106") {
                            this.error_3 = true
                            this.email = ""
                            this.$refs.email.focus();
                        }
                    })
                }
                else if (response.ok) {
                   response.json().then(data =>
                     localStorage.setItem('auth_token', data['token']));
                   window.location = "/";
                }
            })
        },
    }
});

export default Page2;
