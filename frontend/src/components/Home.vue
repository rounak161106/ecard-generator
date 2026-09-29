<template>
  <div class="landing">
    <h1>E-Card Generator</h1>

    <p>Create digital versions of important ID cards easily.</p>

    <div class="card-types">
      <div class="card">
        <h2>Aadhaar Card</h2>
        <p>Generate your Aadhaar card</p>
        <button>Generate</button>
      </div>

      <div class="card">
        <h2>PAN Card</h2>
        <p>Generate your PAN card</p>
        <button>Generate</button>
      </div>

      <div class="card">
        <h2>Voter ID</h2>
        <p>Generate your Voter ID</p>
        <button>Generate</button>
      </div>

      <div class="card">
        <h2>Driving Licence</h2>
        <p>Generate your Driving Licence</p>
        <button>Generate</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.landing {
  text-align: center;
  padding: 60px 20px;
}

.landing h1 {
  font-size: 40px;
  margin-bottom: 10px;
}

.landing > p {
  color: #666;
  margin-bottom: 40px;
}

.card-types {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.card {
  width: 220px;
  padding: 25px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.card h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.card p {
  color: #777;
  font-size: 14px;
}

.card button {
  margin-top: 15px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background: #42b883;
  color: white;
  cursor: pointer;
}

.card button:hover {
  background: #369f6e;
}
</style>