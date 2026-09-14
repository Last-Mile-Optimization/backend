const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("predictionForm");
const volumePreview = document.getElementById("volumePreview");
const loadingOverlay = document.getElementById("loadingOverlay");
const apiStatus = document.getElementById("apiStatus");
const segmentedOptions = document.querySelectorAll(".segmented-option");
const sameCityInput = document.getElementById("sameCity");
const fillExample = document.getElementById("fillExample");


/* =========================================================
   CÁLCULO AUTOMÁTICO DO VOLUME
   ========================================================= */

function calcVolume() {
    const height = Number(
        document.getElementById("height").value || 0
    );

    const width = Number(
        document.getElementById("width").value || 0
    );

    const length = Number(
        document.getElementById("length").value || 0
    );

    const volume = height * width * length;

    volumePreview.textContent =
        `${volume.toLocaleString("pt-BR", {
            maximumFractionDigits: 1
        })} cm³`;

    return volume;
}


["height", "width", "length"].forEach(id => {

    document
        .getElementById(id)
        .addEventListener("input", calcVolume);

});


/* =========================================================
   CAMPO "MESMA CIDADE"
   ========================================================= */

segmentedOptions.forEach(button => {

    button.addEventListener("click", () => {

        segmentedOptions.forEach(option => {
            option.classList.remove("active");
        });

        button.classList.add("active");

        sameCityInput.value = button.dataset.value;
    });

});


/* =========================================================
   BOTÃO PARA PREENCHER UM EXEMPLO
   ========================================================= */

fillExample.addEventListener("click", () => {

    const example = {
        purchaseDate: "2026-09-18",
        purchaseTime: "19:25",
        price: 349.90,
        freightValue: 47.50,
        weight: 2350,
        height: 18,
        width: 32,
        length: 41,
        distance: 612.4,
        sameCity: "0"
    };


    Object.entries(example).forEach(([key, value]) => {

        const element = document.getElementById(key);

        if (element) {
            element.value = value;
        }

    });


    segmentedOptions.forEach(button => {

        button.classList.toggle(
            "active",
            button.dataset.value === example.sameCity
        );

    });


    calcVolume();
});


/* =========================================================
   VERIFICA SE O BACKEND ESTÁ FUNCIONANDO
   ========================================================= */

async function checkApi() {

    try {

        const response = await fetch(
            `${API_URL}/health`,
            {
                signal: AbortSignal.timeout(1800)
            }
        );


        if (!response.ok) {
            throw new Error();
        }


        apiStatus.className = "api-status online";

        apiStatus.innerHTML = `
            <span class="status-dot"></span>
            <span>Backend conectado</span>
        `;

    } catch {

        apiStatus.className = "api-status offline";

        apiStatus.innerHTML = `
            <span class="status-dot"></span>
            <span>Modo demonstração</span>
        `;

    }
}


/* =========================================================
   TELA DE CARREGAMENTO
   ========================================================= */

function showLoading() {

    loadingOverlay.classList.remove("hidden");

    const steps = [
        ...document.querySelectorAll(".loading-step")
    ];


    steps.forEach(step => {
        step.classList.remove("active");
    });


    steps[0].classList.add("active");


    steps.slice(1).forEach((step, index) => {

        setTimeout(() => {

            steps.forEach(item => {
                item.classList.remove("active");
            });

            step.classList.add("active");

        }, (index + 1) * 600);

    });

}


/* =========================================================
   MONTA O JSON QUE SERÁ ENVIADO AO BACKEND
   ========================================================= */

function buildPayload() {

    return {

        purchase_date:
            document.getElementById("purchaseDate").value,

        purchase_time:
            document.getElementById("purchaseTime").value,

        price:
            Number(
                document.getElementById("price").value
            ),

        freight_value:
            Number(
                document.getElementById("freightValue").value
            ),

        product_weight_g:
            Number(
                document.getElementById("weight").value
            ),

        height_cm:
            Number(
                document.getElementById("height").value
            ),

        width_cm:
            Number(
                document.getElementById("width").value
            ),

        length_cm:
            Number(
                document.getElementById("length").value
            ),

        distance_km:
            Number(
                document.getElementById("distance").value
            ),

        same_city:
            Number(sameCityInput.value)
    };
}


/* =========================================================
   MODO DEMONSTRAÇÃO

   Essa função existe para o front-end funcionar mesmo
   antes da integração com o modelo real.

   IMPORTANTE:
   Estes valores NÃO são resultados reais do modelo do TCC.
   ========================================================= */

function demoPrediction(payload) {

    const volume =
        payload.height_cm *
        payload.width_cm *
        payload.length_cm;


    const date = new Date(
        `${payload.purchase_date}T${payload.purchase_time}:00`
    );


    const hour = date.getHours();

    const day = date.getDay();

    const weekend =
        [0, 6].includes(day) ? 1 : 0;


    /*
       Cálculo fictício apenas para demonstração
       visual do sistema.
    */

    let score = 0.16;


    score +=
        Math.min(
            payload.distance_km / 1500,
            1
        ) * 0.28;


    score +=
        Math.min(
            payload.freight_value /
            Math.max(payload.price, 1),
            0.5
        ) * 0.18;


    score +=
        Math.min(
            payload.product_weight_g / 12000,
            1
        ) * 0.10;


    score +=
        Math.min(
            volume / 120000,
            1
        ) * 0.08;


    score += weekend * 0.08;


    score +=
        payload.same_city
            ? -0.06
            : 0.08;


    score +=
        hour >= 18
            ? 0.03
            : 0;


    score = Math.max(
        0.05,
        Math.min(0.96, score)
    );


    /* =====================================================
       COMPARAÇÃO SIMULADA ENTRE MODELOS
       ===================================================== */

    const variants = [

        [
            "Deep Learning",
            score
        ],

        [
            "Random Forest",
            Math.max(
                0.03,
                Math.min(
                    0.97,
                    score + 0.05
                )
            )
        ],

        [
            "XGBoost",
            Math.max(
                0.03,
                Math.min(
                    0.97,
                    score + 0.08
                )
            )
        ],

        [
            "Árvore de Decisão",
            Math.max(
                0.03,
                Math.min(
                    0.97,
                    score - 0.04
                )
            )
        ],

        [
            "KNN",
            Math.max(
                0.03,
                Math.min(
                    0.97,
                    score - 0.12
                )
            )
        ]

    ];


    /* =====================================================
       FATORES QUE INFLUENCIARAM A PREVISÃO
       ===================================================== */

    const factors = [

        [
            "Distância da entrega",
            Math.min(
                100,
                Math.round(
                    (payload.distance_km / 900) * 100
                )
            )
        ],

        [
            "Valor do frete",
            Math.min(
                100,
                Math.round(
                    (
                        payload.freight_value /
                        Math.max(payload.price, 1)
                    ) * 170
                )
            )
        ],

        [
            "Peso do produto",
            Math.min(
                100,
                Math.round(
                    (
                        payload.product_weight_g /
                        5000
                    ) * 100
                )
            )
        ],

        [
            "Volume do produto",
            Math.min(
                100,
                Math.round(
                    (
                        volume /
                        70000
                    ) * 100
                )
            )
        ],

        [
            "Fim de semana",
            weekend
                ? 62
                : 18
        ]

    ].sort(
        (a, b) => b[1] - a[1]
    );


    /* =====================================================
       CLUSTER SIMULADO PARA K-MEANS
       ===================================================== */

    let cluster;


    if (payload.distance_km > 500) {

        cluster = {

            name:
                "Pedidos de longa distância",

            description:
                "Entregas com maior deslocamento entre vendedor e cliente.",

            stats: [

                [
                    "Distância média",
                    "684 km"
                ],

                [
                    "Frete médio",
                    "R$ 52,40"
                ],

                [
                    "Atrasos no grupo",
                    "37%"
                ]

            ]
        };

    }

    else if (
        payload.product_weight_g > 5000
    ) {

        cluster = {

            name:
                "Pedidos pesados de média distância",

            description:
                "Produtos de maior peso com deslocamento intermediário.",

            stats: [

                [
                    "Peso médio",
                    "6,8 kg"
                ],

                [
                    "Frete médio",
                    "R$ 61,20"
                ],

                [
                    "Atrasos no grupo",
                    "31%"
                ]

            ]
        };

    }

    else {

        cluster = {

            name:
                "Pedidos urbanos e leves",

            description:
                "Entregas de menor porte e menor deslocamento.",

            stats: [

                [
                    "Distância média",
                    "96 km"
                ],

                [
                    "Frete médio",
                    "R$ 24,10"
                ],

                [
                    "Atrasos no grupo",
                    "14%"
                ]

            ]
        };

    }


    /* =====================================================
       RETORNO DO RESULTADO SIMULADO
       ===================================================== */

    return {

        analysis_id:
            "DEMO-" +
            Math.random()
                .toString(36)
                .slice(2, 8)
                .toUpperCase(),


        prediction:
            score >= 0.5
                ? 1
                : 0,


        probability:
            score,


        main_model:
            "Deep Learning",


        risk_level:

            score < 0.30
                ? "Baixo"

                : score < 0.61
                    ? "Moderado"

                    : score < 0.81
                        ? "Alto"

                        : "Muito alto",


        models:

            variants.map(
                ([name, probability]) => ({

                    name,

                    probability,

                    prediction:
                        probability >= 0.5
                            ? 1
                            : 0

                })
            ),


        factors:

            factors.map(
                ([name, impact]) => ({

                    name,
                    impact

                })
            ),


        cluster,


        /* =================================================
           DBSCAN
           ================================================= */

        dbscan: {

            is_outlier:

                payload.distance_km > 1200 ||

                payload.product_weight_g > 12000,


            text:

                payload.distance_km > 1200 ||

                payload.product_weight_g > 12000

                    ? "Este pedido apresenta características incomuns em relação aos pedidos históricos."

                    : "Este pedido está dentro de um padrão conhecido nos dados históricos."

        },


        /* =================================================
           PCA
           ================================================= */

        pca_point: {

            x: Math.max(
                -2.5,
                Math.min(
                    2.5,
                    (
                        payload.distance_km - 350
                    ) / 250
                )
            ),

            y: Math.max(
                -2.2,
                Math.min(
                    2.2,
                    (
                        payload.product_weight_g - 2500
                    ) / 1800
                )
            )

        },


        features: {

            purchase_hour:
                hour,

            purchase_day_of_week:
                day,

            is_weekend:
                weekend,

            volume_cm3:
                volume

        },


        input:
            payload,


        demo_mode:
            true
    };
}


/* =========================================================
   ENVIO DO FORMULÁRIO
   ========================================================= */

form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const payload =
            buildPayload();


        showLoading();


        let result;


        try {

            /*
               Tenta utilizar o backend real.
            */

            const response = await fetch(
                `${API_URL}/predict`,
                {

                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(payload)

                }
            );


            if (!response.ok) {

                throw new Error(
                    "Backend indisponível"
                );

            }


            result =
                await response.json();

        }

        catch {

            /*
               Se o backend não estiver rodando,
               utiliza o modo demonstração.
            */

            result =
                demoPrediction(payload);

        }


        /*
           Guarda o resultado temporariamente
           para a página resultado.html.
        */

        sessionStorage.setItem(
            "predictionResult",
            JSON.stringify(result)
        );


        /*
           Pequeno delay para permitir que
           a animação seja exibida.
        */

        setTimeout(() => {

            window.location.href =
                "resultado.html";

        }, 2300);

    }
);


/* =========================================================
   INICIALIZAÇÃO
   ========================================================= */

checkApi();

calcVolume();