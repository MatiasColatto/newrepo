import http from 'k6/http';
import { check, sleep } from 'k6';


export const options = {

    stages: [
        { duration: '30s', target: 10 },
        { duration: '1m', target: 50 },
        { duration: '30s', target: 0 },
    ],

    thresholds: {
        http_req_duration: [
            'p(95)<500'
        ],
        http_req_failed: [
            'rate<0.01'
        ]
    }
};


// Simulación de login
function login() {

    const user = {
        username: "demo",
        password: "123456"
    };


    // Simulamos respuesta del backend
    const fakeToken =
        "eyJhbGciOiJIUzI1NiJ9.demo-token";


    check(user, {
        "login enviado": (u) =>
            u.username === "demo"
    });


    return fakeToken;
}



export default function () {


    // 1. Login
    let token = login();


    check(token,{
        "token generado":
            (t)=> t.length > 0
    });



    // 2. Usar token contra PetClinic
    let owners = http.get(
        "http://localhost:8080/owners/find",
        {
            headers:{
                Authorization:
                `Bearer ${token}`
            }
        }
    );


    check(owners,{
        "owners OK":
            (r)=>r.status === 200
    });



    // 3. Otro endpoint protegido simulado
    let vets = http.get(
        "http://localhost:8080/vets.html",
        {
            headers:{
                Authorization:
                `Bearer ${token}`
            }
        }
    );


    check(vets,{
        "vets OK":
            (r)=>r.status === 200
    });


    sleep(1);
}