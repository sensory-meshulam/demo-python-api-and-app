console.log("blabla")

const apiUrl = 'http://localhost:5000';
let resultStatus; //boolean
let resultData;


const data =  {
    sum: 1,
    paymentsNum: 1,
    description: "The destination of the payment",
  }
  
const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Request-Method": "POST",
      "Access-Control-Request-Headers": "Content-Type",
    },
    body: JSON.stringify(data)
}

async function getPaymentLink (){
   const response = await fetch(`/api/payment/getPaymentLink`, options);
   //response in format {isSuccess: boolean, message: string (payment-link or error-message)}
   const data = await response.json();
   console.log(data.message)
   growPayment.renderPaymentOptions(data.message)
}

window.addEventListener("growWalletChange", (result) => {
    console.log("result:", result.detail);
    let res = result.detail;
    if (res.status === 1) {
      resultStatus = true;
      resultData = res.data;
    }
    if (res.state === "close" && resultStatus) {
      // Now you can access the success page, and also send data to it via the URL
      console.log(resultData);
      const searchParams = new URLSearchParams(resultData);      
      window.open(`http://localhost:5000/static/success.html?${searchParams.toString()}`)
    }
  });