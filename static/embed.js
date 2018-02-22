(function () {
  // add styling
  const style = document.createElement('style');
  style.type = 'text/css';
  style.innerHTML = 'button.raipay { font-family: sans-serif; background: linear-gradient(90deg,#390050, #5a5d9d); border: none; border-radius: 1rem; padding: .5rem 1rem; color: white; cursor: pointer; }';
  document.getElementsByTagName('head')[0].appendChild(style);

  // load settings & create element
  let script = document.querySelector('script[data-vendor]'),
    btn = document.createElement('button');
  btn.setAttribute('class', 'raipay');
  btn.innerHTML = 'Pay with RaiPay';
  script.parentNode.insertBefore(btn, script);

  let vendor = script.getAttribute('data-vendor'),
    amount = script.getAttribute('data-amount'),
    currency = script.getAttribute('data-currency'),
    tag = script.getAttribute('data-tag'),
    redirect_url = script.getAttribute('data-redirect-url'),
    webhook = script.getAttribute('data-webhook');

  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const newXHR = new XMLHttpRequest();
    // "load" is fired when the response to our request is completed and without error.
    newXHR.addEventListener('load', function () {
      const data = JSON.parse(this.response);
      window.location.href = `https://sendkudo.org/api/v1/getbalance/${data.token}`;
    });
    newXHR.open('POST', `http://127.0.0.1:5000/payments/${vendor}`);
    newXHR.setRequestHeader('Content-Type', 'application/json');
    newXHR.send(JSON.stringify({ amount, currency, tag, redirect_url, webhook }));
  });
}());