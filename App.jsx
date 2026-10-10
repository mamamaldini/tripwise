import { useEffect, useMemo, useState } from 'react';
import { ArrowDownRight, ArrowRight, Clock3, Compass, MapPin, RefreshCw, Sparkles, Sun, Wallet, CloudRain, CheckCircle2, AlertTriangle, Navigation } from 'lucide-react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const INTERESTS = ['history', 'architecture', 'photography', 'culture', 'nature', 'museum', 'science'];
const fallback = [
  { id: 'city-palace', name: 'City Palace', description: 'Palace complex, museums, and ornate courtyards in the old city.', categories: ['history','architecture','culture','photography'], crowd_percent: 23, travel_minutes: 18, visit_minutes: 75, cost_inr: 300, outdoors: false, action: 'GO', score: 86.4, reasons: ['Crowd estimate is within your preferred limit','Matches your interests','Relatively short estimated journey'], data_mode: 'simulated_demo_data' },
  { id: 'jal-mahal', name: 'Jal Mahal', description: 'Lakeside palace viewpoint, especially atmospheric near sunset.', categories: ['photography','nature','architecture'], crowd_percent: 45, travel_minutes: 22, visit_minutes: 35, cost_inr: 0, outdoors: true, action: 'GO', score: 78.1, reasons: ['Crowd estimate is within your preferred limit','Estimated entry cost fits your budget'], data_mode: 'simulated_demo_data' },
  { id: 'amber-fort', name: 'Amber Fort', description: 'Hilltop fort with courtyards and historic architecture.', categories: ['history','architecture','photography'], crowd_percent: 78, travel_minutes: 35, visit_minutes: 120, cost_inr: 500, outdoors: true, action: 'AVOID', score: 61.2, reasons: ['Crowd estimate is above your preferred limit','Matches your interests'], data_mode: 'simulated_demo_data' },
];

function crowdLabel(value) { return value < 35 ? 'Quiet' : value < 65 ? 'Moderate' : 'Busy'; }
function App() {
  const [city, setCity] = useState('Jaipur');
  const [interests, setInterests] = useState(['history', 'architecture', 'photography']);
  const [minutes, setMinutes] = useState(240);
  const [budget, setBudget] = useState(1000);
  const [maxCrowd, setMaxCrowd] = useState(65);
  const [weather, setWeather] = useState('clear');
  const [places, setPlaces] = useState(fallback);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState('demo');
  const [summary, setSummary] = useState('A quieter heritage stop can make the rest of your afternoon feel effortless.');
  const [toast, setToast] = useState('');

  const top = useMemo(() => places.find(p => p.action === 'GO') || places[0], [places]);
  async function refresh() {
    setLoading(true);
    try {
      const response = await fetch(`${API}/api/recommendations`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ city, interests, available_minutes: minutes, budget_inr: budget, max_crowd_percent: maxCrowd, weather, prefer_outdoors: weather !== 'rain' }) });
      if (!response.ok) throw new Error('API unavailable');
      const data = await response.json();
      setPlaces(data.recommendations);
      setApiStatus('connected');
      setToast('Recommendations refreshed');
      try {
        const s = await fetch(`${API}/api/summary`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ city, interests, available_minutes: minutes, budget_inr: budget, max_crowd_percent: maxCrowd, weather, prefer_outdoors: weather !== 'rain' }) });
        if (s.ok) setSummary((await s.json()).summary);
      } catch { /* The deterministic recommendation results remain available. */ }
    } catch {
      setPlaces(fallback.map(p => ({ ...p, action: p.crowd_percent > maxCrowd ? (p.crowd_percent > 80 ? 'AVOID' : 'ALTERNATIVE') : 'GO' })).sort((a,b) => (a.action !== 'GO') - (b.action !== 'GO') || b.score - a.score));
      setApiStatus('demo');
      setToast('Using offline demo data');
    } finally {
      setLoading(false);
      window.setTimeout(() => setToast(''), 2400);
    }
  }
  useEffect(() => { refresh(); /* initial load */ }, []); // eslint-disable-line react-hooks/exhaustive-deps

  function toggleInterest(value) { setInterests(current => current.includes(value) ? current.filter(x => x !== value) : [...current, value]); }
  function actionMeta(action) {
    if (action === 'GO') return { label: 'GO NOW', className: 'go', icon: CheckCircle2 };
    if (action === 'AVOID') return { label: 'AVOID NOW', className: 'avoid', icon: AlertTriangle };
    return { label: 'TRY ALTERNATIVE', className: 'alt', icon: ArrowDownRight };
  }

  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#top"><span className="brand-mark"><Compass size={20}/></span><span>tripwise<span className="brand-dot">.</span></span></a><nav><a href="#discover">Discover</a><a href="#how">How it works</a></nav><div className="top-actions"><span className="live-dot"/><span className="status-label">{apiStatus === 'connected' ? 'API CONNECTED' : 'DEMO MODE'}</span><button className="avatar" aria-label="Traveler profile">T</button></div></header>
    <main id="top">
      <section className="hero"><div className="hero-copy"><div className="eyebrow"><span className="eyebrow-line"/> THE CITY IS YOURS TO DISCOVER</div><h1>Travel less blindly.<br/><em>Decide smarter.</em></h1><p>Skip the guesswork. Find the right place to visit <strong>right now</strong>, with crowd-aware recommendations built around your day.</p><div className="hero-meta"><span><MapPin size={15}/> Jaipur, India</span><span><Sun size={15}/> Your day, optimized</span></div><a className="scroll-link" href="#discover">Explore your next stop <ArrowDownRight size={16}/></a></div><div className="hero-art"><div className="sun-disc"/><div className="hill hill-back"/><div className="hill hill-front"/><div className="fort-silhouette"><div className="fort-roof"/><div className="fort-body"><span/><span/><span/><span/><span/></div><div className="fort-base"/></div><div className="art-label"><span className="live-dot"/> YOUR NEXT CHAPTER <span className="label-divider"/> 26.92° N</div><div className="floating-note"><span className="note-icon"><Sparkles size={16}/></span><div><b>Better choices, less waiting</b><small>One smart stop at a time</small></div></div></div></section>
      <section className="dashboard" id="discover"><div className="section-heading"><div><div className="eyebrow"><span className="eyebrow-line"/> YOUR LIVE DECISION BOARD</div><h2>Where to next?</h2><p>Tell us what matters today. We'll help you make the most of it.</p></div><button className="refresh-button" onClick={refresh} disabled={loading}><RefreshCw size={15} className={loading ? 'spin' : ''}/>{loading ? 'Updating' : 'Refresh advice'}</button></div>
        <div className="workspace"><aside className="preferences panel"><div className="panel-title"><span className="title-icon"><Compass size={17}/></span><div><h3>Your day, your way</h3><p>Fine-tune your recommendations</p></div></div><label className="field-label" htmlFor="city">DESTINATION</label><div className="select-wrap"><MapPin size={16}/><select id="city" value={city} onChange={e => setCity(e.target.value)}><option>Jaipur</option><option>Delhi</option><option>Mumbai</option><option>Goa</option><option>Agra</option></select></div><div className="field-row"><label className="field-label" htmlFor="time">TIME LEFT</label><span className="field-value">{minutes >= 60 ? `${Math.floor(minutes/60)}h${minutes%60 ? ` ${minutes%60}m` : ''}` : `${minutes}m`}</span></div><input id="time" className="range" type="range" min="30" max="600" step="30" value={minutes} onChange={e => setMinutes(Number(e.target.value))}/><div className="range-captions"><span>30 min</span><span>10 hours</span></div><div className="field-row"><label className="field-label" htmlFor="budget">ENTRY BUDGET</label><span className="field-value">₹{budget.toLocaleString('en-IN')}</span></div><input id="budget" className="range" type="range" min="0" max="3000" step="100" value={budget} onChange={e => setBudget(Number(e.target.value))}/><div className="range-captions"><span>Free</span><span>₹3,000+</span></div><div className="field-row"><span className="field-label">WEATHER</span></div><div className="weather-options"><button className={weather === 'clear' ? 'weather-choice selected' : 'weather-choice'} onClick={() => setWeather('clear')}><Sun size={16}/> Clear</button><button className={weather === 'cloudy' ? 'weather-choice selected' : 'weather-choice'} onClick={() => setWeather('cloudy')}><span>☁</span> Cloudy</button><button className={weather === 'rain' ? 'weather-choice selected' : 'weather-choice'} onClick={() => setWeather('rain')}><CloudRain size={16}/> Rain</button></div><div className="field-label interest-label">YOUR INTERESTS</div><div className="interest-tags">{INTERESTS.map(item => <button key={item} className={interests.includes(item) ? 'interest selected' : 'interest'} onClick={() => toggleInterest(item)}>{item}</button>)}</div><button className="primary-button full" onClick={refresh} disabled={loading}>{loading ? 'Finding your next stop…' : 'Find my next stop'} <ArrowRight size={16}/></button><p className="privacy-note">Your preferences stay in this demo session.</p></aside>
          <div className="results-column"><div className="recommendation-banner"><div className="banner-copy"><span className="banner-kicker"><Sparkles size={13}/> TRIPWISE RECOMMENDS</span><h3>{top?.name || 'Your next stop'}</h3><p>{top?.description || 'Choose your preferences to get started.'}</p><div className="banner-tags"><span><Clock3 size={13}/> {top?.travel_minutes ?? '—'} min away</span><span><Wallet size={13}/> ₹{top?.cost_inr ?? '—'} entry</span></div></div><div className="score-ring" style={{'--score': `${top?.score || 0}%`}}><div><b>{Math.round(top?.score || 0)}</b><small>FIT SCORE</small></div></div><div className="banner-bottom"><span className="recommend-pill"><CheckCircle2 size={14}/> SMART PICK</span><span>Based on your preferences + demo conditions</span></div></div>
            <div className="list-heading"><div><h3>Other places to consider</h3><p>Ranked for your current plans</p></div><span className="result-count">{places.length} PLACES</span></div><div className="place-list">{places.map((place, index) => { const meta = actionMeta(place.action); const Icon = meta.icon; return <article className={`place-card ${index === 0 ? 'first-place' : ''}`} key={place.id}><div className={`place-number ${meta.className}`}>{String(index+1).padStart(2,'0')}</div><div className="place-main"><div className="place-title-row"><h4>{place.name}</h4><span className={`action-badge ${meta.className}`}><Icon size={12}/>{meta.label}</span></div><p>{place.description}</p><div className="place-stats"><span><Clock3 size={13}/>{place.travel_minutes} min travel</span><span className={`crowd-text crowd-${crowdLabel(place.crowd_percent).toLowerCase()}`}><span className="crowd-dot"/>{crowdLabel(place.crowd_percent)} · {place.crowd_percent}%</span><span><Wallet size={13}/>₹{place.cost_inr}</span></div><div className="reason-line">{place.reasons?.[0]}</div></div><div className="mini-score"><b>{Math.round(place.score)}</b><small>FIT</small></div></article>; })}</div><div className="data-note"><AlertTriangle size={15}/><span><b>Demo data:</b> Crowd percentages and travel times are illustrative estimates, not live sensor or traffic measurements.</span></div></div></div>
      </section>
      <section className="insight-strip"><div className="insight-icon"><Sparkles size={18}/></div><div><span className="eyebrow">A LITTLE TRAVEL WISDOM</span><p>{summary}</p></div><span className="insight-decoration">✳</span></section>
      <section className="how-section" id="how"><div className="eyebrow"><span className="eyebrow-line"/> FROM GUESSWORK TO GOOD DAYS</div><h2>Three steps. Better stories.</h2><div className="steps"><article><span>01</span><MapPin/><h3>Know your moment</h3><p>Set your time, budget, interests, and weather preferences.</p></article><article><span>02</span><Sparkles/><h3>Weigh the options</h3><p>TripWise scores crowd estimates, travel time, and how well each place fits your plans.</p></article><article><span>03</span><Navigation/><h3>Go with confidence</h3><p>Get a clear next stop and alternatives, with reasons you can understand.</p></article></div></section>
    </main><footer><a className="brand" href="#top"><span className="brand-mark"><Compass size={18}/></span><span>tripwise<span className="brand-dot">.</span></span></a><span>Travel less blindly. Decide smarter.</span><span>Built for curious people, everywhere. ✳</span></footer>{toast && <div className="toast" role="status">{toast}</div>}
  </div>;
}
export default App;
