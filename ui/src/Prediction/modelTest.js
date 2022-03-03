import React, { useEffect, useState , PureComponent } from 'react';
import { PieChart, Pie , ResponsiveContainer} from 'recharts';

// JS
// const input = document.getElementById('myText');
// const inputValue = input.value
// React
// value, onChange

const ModelTest = () => {
  // Input Variables
  const [arg1, setArg1] = useState('10');
  const [arg2, setArg2] = useState('10');
  const [arg3, setArg3] = useState('10');
  const [arg4, setArg4] = useState('10');
  const data = [
    {name: 'Geeksforgeeks', students: 400},
    {name: 'Technical scripter', students: 700},
    {name: 'Geek-i-knack', students: 200},
    {name: 'Geek-o-mania', students: 1000}
  ];

  const dataValues = [{ name: 'ARG1',msgCount: 15 },
                    { name: 'ARG2',msgCount: 45 },
                    { name: 'ARG3',msgCount: 23},
                    { name: 'ARG4',msgCount: 22}]
 

  
  useEffect(() => {
      console.log(dataValues)
        dataValues[0].msgCount = parseInt(arg1);
        dataValues[1].msgCount = parseInt(arg2);
        dataValues[2].msgCount = parseInt(arg3);
        dataValues[3].msgCount = parseInt(arg4);
           }
        );
    console.log('useEffectEveryReRender ')


  const handleSubmit = (e) => {
    e.preventDefault();
    if (arg1 && arg2 && arg3 && arg4) {
      const algoInput = { arg1, arg2, arg3, arg4 };
      console.log(algoInput);
      setArg1('');
      setArg2('');
      setArg3('');
      setArg4('');
    } else {
       console.log('Fill all mandatory attributes..');
    }
  };
 
  return (
    <>
    <div className="container">
    <div className="inputArgs">
    <article>
        <form className='form' onSubmit={handleSubmit}>
          <div className='form-control'>
            <label htmlFor='arg1'>Value Arg1 : </label>
            <input id='arg1' type='number' min="0"
              name='arg1' value={arg1}
              onChange={(e) => setArg1(e.target.value)}
            />
          </div>
          <div className='form-control'>
            <label htmlFor='arg2'>Value Arg2 : </label>
            <input id='arg2' type='number' min="0"
              name='arg2' value={arg2}
              onChange={(e) => setArg2(e.target.value)}
            />
          </div>
          <div className='form-control'>
            <label htmlFor='arg3'>Value Arg3 : </label>
            <input id='arg3' type='number' min="0"
              name='arg3' value={arg3}
              onChange={(e) => setArg3(e.target.value)}
            />
          </div>
          <div className='form-control'>
            <label htmlFor='arg4'>Value Arg4 : </label>
            <input id='arg4' type='number' min="0"
              name='arg4' value={arg4}
              onChange={(e) => setArg4(e.target.value)}
            />
          </div>
          <button type='submit'>Submit</button>
        </form>
      </article>
    </div>
    <div className="inputSlider">
   
    </div>
    <div className="pieplot">
    <ResponsiveContainer>
    <PieChart width={600} height={400}>
          <Pie data={dataValues} nameKey="name" dataKey="msgCount" outerRadius={150} innerRadius={100} fill="green" />
    </PieChart>
    </ResponsiveContainer>
    </div>
    <div className="output"></div>
    <div className="details"></div>
    </div>
    
    </>
  );

};

export default ModelTest;
