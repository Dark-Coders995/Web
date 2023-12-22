const Page1 = Vue.component("login",{

    data :function(){
        return{
            user_name :"",
            password:"",
            error_1: false,
            error_2: false
        }
    },
    template: `
        <div class="login-card">
            <h2 class="text-center mb-4">User Login</h2>
            <form @submit.prevent="login">
                <div class="form-group">
                    <label for="user_name">Username</label>
                    <input v-model="user_name" class="form-control" id="user_name" name="user_name" required type="text">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input v-model="password" class="form-control" id="password" name="password" required type="password">
                </div>
                <button class="btn btn-primary w-100" type="submit">Login</button>
            </form>
            <p class="mt-3">Don't have an account? <router-link to="/sign_up">Sign up</router-link></p>
            <router-link to="/manager_login">Manager Login</router-link>
        </div>
        `,

    methods:{
        login() {
            this.error = "";
            const user_name = this.user_name;
            const password = this.password;
            var url = `/api/login/${user_name}/${password}`;
            console.log(url);

            fetch(url, {
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
                  this.$router.push('/user_logged');
                }
            })
        },
}
});

export default Page1;
