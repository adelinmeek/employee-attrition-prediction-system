import { useState } from "react";
const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";
const initial = { Education:"Bachelors", JoiningYear:"2022", City:"Bangalore", PaymentTier:"2", Age:"28", Gender:"Male", EverBenched:"No", ExperienceInCurrentDomain:"2" };
function App() {
 const [form,setForm]=useState(initial), [loading,setLoading]=useState(false), [error,setError]=useState(""), [result,setResult]=useState(null);
 const change=e=>{setForm(p=>({...p,[e.target.name]:e.target.value}));setError("");};
 async function submit(e) {
  e.preventDefault();setLoading(true);setError("");setResult(null);
  const payload={...form,JoiningYear:Number(form.JoiningYear),PaymentTier:Number(form.PaymentTier),Age:Number(form.Age),ExperienceInCurrentDomain:Number(form.ExperienceInCurrentDomain)};
  try {
   const res=await fetch(`${API}/predict`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
   const data=await res.json().catch(()=>({}));
   if(!res.ok) throw new Error(data.error||"Prediction request failed.");
   if(data.prediction===undefined) throw new Error("API response did not include a prediction.");
   setResult({leave:Number(data.prediction)===1,prob:data.probability_leave,message:data.message});
  } catch(err) {setError(err.message==="Failed to fetch"?"Cannot connect to Flask. Start backend/app.py first.":err.message);}
  finally {setLoading(false);}
 }
 const select=(label,name,options)=><div className="field"><label htmlFor={name}>{label}</label><select id={name} name={name} value={form[name]} onChange={change} required>{options.map(o=><option key={o[0]} value={o[0]}>{o[1]}</option>)}</select></div>;
 const number=(label,name,min,max)=><div className="field"><label htmlFor={name}>{label}</label><input id={name} name={name} type="number" min={min} max={max} value={form[name]} onChange={change} required /></div>;
 return <main className="shell">
  <header className="nav"><div className="logo">PI</div><div><strong>PeopleInsight</strong><small>Employee analytics</small></div><span className="pill">ATTRITION PREDICTION</span></header>
  <section className="hero"><p className="eyebrow">WORKFORCE INTELLIGENCE</p><h1>Understand employee <span>attrition.</span></h1><p>Enter an employee profile to get a prediction from your trained machine-learning model.</p></section>
  <section className="layout"><div className="panel"><div className="heading"><div><p className="kicker">EMPLOYEE PROFILE</p><h2>Employee details</h2><p className="muted">Complete all fields to run a prediction.</p></div><span className="step">01 / 01</span></div>
   <form onSubmit={submit}><div className="fields">
    {select("Education","Education",[["Bachelors","Bachelors"],["Masters","Masters"],["PHD","PhD"]])}
    {number("Joining year","JoiningYear",2000,new Date().getFullYear())}
    {select("Work city","City",[["Bangalore","Bangalore"],["Pune","Pune"],["New Delhi","New Delhi"]])}
    {select("Payment tier","PaymentTier",[["1","Tier 1"],["2","Tier 2"],["3","Tier 3"]])}
    {number("Age","Age",18,100)}
    {select("Gender","Gender",[["Male","Male"],["Female","Female"]])}
    {select("Ever benched?","EverBenched",[["No","No"],["Yes","Yes"]])}
    {number("Domain experience (years)","ExperienceInCurrentDomain",0,50)}
   </div>
   {error&&<div className="error" role="alert"><b>Prediction failed</b><span>{error}</span></div>}
   <div className="actions"><button type="button" className="secondary" onClick={()=>{setForm(initial);setError("");setResult(null);}} disabled={loading}>Reset form</button><button className="primary" disabled={loading}>{loading?"Analyzing…":"Predict attrition →"}</button></div>
   </form></div>
   <aside className="panel result"><p className="kicker">PREDICTION RESULT</p>{!result?<div className="empty"><div className="art">✳</div><h2>Your results appear here</h2><p>Complete the profile and run the model to see its prediction.</p><div className="notice">Predictions require a trained model in the Flask backend.</div></div>:<div className="outcome"><p className="kicker">MODEL PREDICTION</p><div className={`symbol ${result.leave?"leave":"stay"}`}>{result.leave?"!":"✓"}</div><h2>{result.leave?"May leave":"May stay"}</h2><p>{result.leave?"The model predicts that this employee may leave.":"The model predicts that this employee may stay."}</p>{result.prob!=null&&<div className="prob"><div><span>Estimated leave probability</span><b>{(Number(result.prob)*100).toFixed(1)}%</b></div><div className="track"><span style={{width:`${Math.max(0,Math.min(100,Number(result.prob)*100))}%`}} /></div></div>}<div className="notice">{result.message||"This is a statistical estimate, not a certainty."}</div></div>}</aside>
  </section><footer><span>PeopleInsight · Employee Attrition Prediction</span><span>Educational decision-support demo</span></footer>
 </main>;
}
export default App;
