

# npm package installs :

 -  npm install recharts
   https://www.geeksforgeeks.org/create-a-donut-chart-using-recharts-in-reactjs/  
   




##  Pie Chart component ref
https://www.npmjs.com/package/react-minimal-pie-chart  

## Grid design

https://grid.layoutit.com/
HTML:  

```
<div class="container">
  <div class="inputArgs"></div>
  <div class="inputSlider"></div>
  <div class="pieplot"></div>
  <div class="output"></div>
  <div class="details"></div>
</div>
```


CSS:  
```
.container {  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr;
  gap: 0px 0px;
  grid-auto-flow: row;
  grid-template-areas:
    "details details details"
    "inputArgs inputSlider pieplot"
    "output output output";
}

.inputArgs { grid-area: inputArgs; }

.inputSlider { grid-area: inputSlider; }

.pieplot { grid-area: pieplot; }

.output { grid-area: output; }

.details { grid-area: details; }

```
