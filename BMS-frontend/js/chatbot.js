(function(){
  const form=document.querySelector("[data-chat-form]");
  const input=document.querySelector("[data-chat-input]");
  const body=document.querySelector("[data-chat-body]");
  if(!form||!input||!body) return;
  form.addEventListener("submit", async e=>{
    e.preventDefault();
    const text=input.value.trim(); if(!text) return;
    const u=document.createElement("div"); u.className="user-message"; u.textContent=text; body.appendChild(u); input.value="";
    try{
      const r=await allerApiMessage(text);
      const b=document.createElement("div"); b.className="bot-message"; b.textContent=r; body.appendChild(b);
    }catch(err){
      const b=document.createElement("div"); b.className="bot-message"; b.textContent="ALLER Assist is temporarily unavailable. Please use the relevant banking service menu."; body.appendChild(b);
    }
    body.scrollTop=body.scrollHeight;
  });
  async function alFlerApiMessage(message){
    const r=await apiRequest("/chatbot/message",{method:"POST",body:JSON.stringify({message})});
    return r.data?.reply || "I can help with ALLER BANK services.";
  }
})();
