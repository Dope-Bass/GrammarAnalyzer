import React, { Component } from "react";
import "./App.css";
import axios from 'axios';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: "",
      analyzeText: [],
      bool: true,
      obj: false,
      sub: false,
      pre: false,
      att: false,
      ad: false,
      loading: false
    };
  }

  InputChange = (event) => {
    this.setState({
      text: event.target.value
    });
  };

  InputFile = async (e) => {
    //if (e!==undefined){
    e.preventDefault();
    const reader = new FileReader();
    reader.onload = async (e) => {
      const text = e.target.result;
      this.setState({
        text: text
      });
    };
    reader.readAsText(e.target.files[0]);
  };

  Delete = () => {
    this.setState({
      text: ""
    });
  };

  EnterKeyPress = (event) => {
    if (event.key === "Enter") {
      this.Analyze();
    }
  };

  Analyze = () => {
    if (this.state.text !== "") {
      //let loading = true;
      
      this.setState({
        loading: true 
      })
      
      axios.post("http://127.0.0.1:8000/analyze/text/",{ text: this.state.text })
        .then((res) => console.log(res))
        .catch((error) => console.log("SOMETHING WENT WRONG ", error))

      .then(() => {
        axios.get("http://127.0.0.1:8000/analyze/words/")
      .then((res) => {
        this.setState({
          analyzeText: res.data
        });
      })
      .then(() => {this.setState({
        bool: false,
        loading: false
      })
      
    });
      
    });

     /* while (this.state.loading === true){
        setTimeout(300);
      }*/
      
     /* sleep(2000)
  .then(() => { console.log("World!"); })*/
      
    } else alert("Введите текст или выберите файл");
  };

  Back = () => {
    //axios.post("http://127.0.0.1:8000/analyze/text/",{ text: "" })
    this.setState({
      bool: true,
      obj: false,
      sub: false,
      pre: false,
      att: false,
      ad: false
    });
  };

  Subject = () => {
    if (this.state.sub === true)
      this.setState({
        sub: false
      });
    else
      this.setState({
        sub: true
      });
  };

  Object = () => {
    if (this.state.obj === true)
      this.setState({
        obj: false
      });
    else
      this.setState({
        obj: true
      });
  };

  Predicate = () => {
    if (this.state.pre === true)
      this.setState({
        pre: false
      });
    else
      this.setState({
        pre: true
      });
  };

  Adverbial_modifier = () => {
    if (this.state.ad === true)
      this.setState({
        ad: false
      });
    else
      this.setState({
        ad: true
      });
  };

  Attribute = () => {
    if (this.state.att === true)
      this.setState({
        att: false
      });
    else
      this.setState({
        att: true
      });
  };

  /*ChangeVal = () => {
    if (this.state.att === true)
      this.setState({
        att: false
      });
    else
      this.setState({
        att: true
      });
  };*/

  /*SelectAll = () => {
    if (this.state.att === true)
      this.setState({
        sub: false,
        obj: false,
        pre: false,
        att: false
      });
    else
      this.setState({
        sub: true,
        obj: true,
        pre: true,
        att: true
      });
  };*/

   /*check = (field, flag) => {
    if (flag==1) { for (var i=0; i<field.length; i++) field[i].checked = true; }
    else { for (i=0; i<field.length; i++) field[i].checked = false; }
   };*/

  render() {
    if (this.state.bool === true && this.state.loading === false) {
      return (
        <div className="App">
          <div className="Zag">
            Введите текст или загрузите текстовый файл (txt,doc,docx)
          </div>
          <div>
            <textarea
              type="text"
              className="inputText"
              placeholder="Введите текст для анализа"
              value={this.state.text}
              onChange={this.InputChange}
              onKeyPress={this.EnterKeyPress}
            />

            <div>
              <input
                type="file"
                className="inputFile"
                accept=".txt,.doc,.docx"
                onChange={(e) => this.InputFile(e)}
              />
            </div>
          </div>
          <button className="button" onClick={this.Analyze}>
            Анализировать
          </button>
          <button className="button" onClick={this.Delete}>
            Стереть
          </button>
        </div>
      );
    } else if (this.state.bool === true && this.state.loading === true) {
      return (
        <div>
          <div id="circularG">
	        <div id="circularG_1" className="circularG"></div>
	        <div id="circularG_2" className="circularG"></div>
	        <div id="circularG_3" className="circularG"></div>
	        <div id="circularG_4" className="circularG"></div>
	        <div id="circularG_5" className="circularG"></div>
	        <div id="circularG_6" className="circularG"></div>
	        <div id="circularG_7" className="circularG"></div>
	        <div id="circularG_8" className="circularG"></div>
          <div className="Zag2">Идет анализ...</div>
          </div>
        </div>
      );
    }
    else {
      return (
        <div className="App">
          <div className="output">
            {this.state.analyzeText.map((postDetail, index) => {
              if (postDetail.role === "дополнение" && this.state.obj === true)
                return (
                  <div className="output_words Object dropdown" key={index}>
                    {postDetail.word}
                    <div className=" dropdown-content">
                      <p>Начальная форма: {postDetail.normal_form}</p>
                      <p>Часть речи: {postDetail.speech_part}</p>
                      <p>Падеж: {postDetail.case}</p>
                      <p>Род: {postDetail.gender}</p>
                      <p>Число: {postDetail.number}</p>
                      <p>Лицо: {postDetail.person}</p>
                      <p>Залог: {postDetail.voice}</p>
                      <p>Член предложения: {postDetail.role}</p>
                    </div>
                  </div>
                );
              if (postDetail.role === "подлежащее" && this.state.sub === true)
                return (
                  <div className="output_words Subject dropdown" key={index}>
                    {postDetail.word}
                    <div className=" dropdown-content">
                      <p>Начальная форма: {postDetail.normal_form}</p>
                      <p>Часть речи: {postDetail.speech_part}</p>
                      <p>Падеж: {postDetail.case}</p>
                      <p>Род: {postDetail.gender}</p>
                      <p>Число: {postDetail.number}</p>
                      <p>Лицо: {postDetail.person}</p>
                      <p>Залог: {postDetail.voice}</p>
                      <p>Член предложения: {postDetail.role}</p>
                    </div>
                  </div>
                );
              if (postDetail.role === "сказуемое" && this.state.pre === true)
                return (
                  <div className="output_words Predicate dropdown" key={index}>
                    {postDetail.word}
                    <div className=" dropdown-content">
                      <p>Начальная форма: {postDetail.normal_form}</p>
                      <p>Часть речи: {postDetail.speech_part}</p>
                      <p>Падеж: {postDetail.case}</p>
                      <p>Род: {postDetail.gender}</p>
                      <p>Число: {postDetail.number}</p>
                      <p>Лицо: {postDetail.person}</p>
                      <p>Залог: {postDetail.voice}</p>
                      <p>Член предложения: {postDetail.role}</p>
                    </div>
                  </div>
                );
              if (postDetail.role === "определение" && this.state.att === true)
                return (
                  <div className="output_words Attribute dropdown" key={index}>
                    {postDetail.word}
                    <div className=" dropdown-content">
                      <p>Начальная форма: {postDetail.normal_form}</p>
                      <p>Часть речи: {postDetail.speech_part}</p>
                      <p>Падеж: {postDetail.case}</p>
                      <p>Род: {postDetail.gender}</p>
                      <p>Число: {postDetail.number}</p>
                      <p>Лицо: {postDetail.person}</p>
                      <p>Залог: {postDetail.voice}</p>
                      <p>Член предложения: {postDetail.role}</p>
                    </div>
                  </div>
                );
              if (postDetail.role === "обстоятельство" && this.state.ad === true)
                return (
                  <div
                    className="output_words Adverbial_modifier dropdown"
                    key={index}
                  >
                    {postDetail.word}
                    <div className=" dropdown-content">
                      <p>Начальная форма: {postDetail.normal_form}</p>
                      <p>Часть речи: {postDetail.speech_part}</p>
                      <p>Падеж: {postDetail.case}</p>
                      <p>Род: {postDetail.gender}</p>
                      <p>Число: {postDetail.number}</p>
                      <p>Лицо: {postDetail.person}</p>
                      <p>Залог: {postDetail.voice}</p>
                      <p>Член предложения: {postDetail.role}</p>
                    </div>
                  </div>
                );
              else
                return (
                  <div className="output_words dropdown" key={index}>
                    {" "}
                    {postDetail.word}
                    <div className=" dropdown-content ">
                      <p>Начальная форма: {postDetail.normal_form}</p>
                      <p>Часть речи: {postDetail.speech_part}</p>
                      <p>Падеж: {postDetail.case}</p>
                      <p>Род: {postDetail.gender}</p>
                      <p>Число: {postDetail.number}</p>
                      <p>Лицо: {postDetail.person}</p>
                      <p>Залог: {postDetail.voice}</p>
                      <p>Член предложения: {postDetail.role}</p>
                    </div>
                  </div>
                );
            })}
          </div>
          <div  className="notInLine">
          
            <input type="checkbox" className="button" onClick={this.Subject} />
            Подлежащее<br></br>
            <input type="checkbox" className="button" onClick={this.Predicate} />
            Сказуемое<br></br>
            <input type="checkbox" className="button" onClick={this.Object} />
            Дополнение<br></br>
            <input type="checkbox" className="button" onClick={this.Attribute} />
            Определение<br></br>
            <input type="checkbox" className="button" onClick={this.Adverbial_modifier} />
            Обстоятельство<br></br>
            
          </div>
          <div>
            <button className="button" onClick={this.Back}>
              Назад
            </button>
          </div>
        </div>
      );
    }
  }
}

export default App;

/*
<form name="select_all" method="post" >
            <input type="checkbox" className="button" name={list} onClick={this.Subject} />
            Подлежащее<br></br>
            <input type="checkbox" className="button" name={list} onClick={this.Predicate} />
            Сказуемое<br></br>
            <input type="checkbox" className="button" name={list} onClick={this.Object} />
            Дополнение<br></br>
            <input type="checkbox" className="button" name={list} onClick={this.Attribute} />
            Определение<br></br>
            <input type="checkbox" className="button" name={list} onClick={this.Adverbial_modifier} />
            Обстоятельство<br></br>
            <input type="button" value="Выделить все" onclick={this.check(this.form.list, 1)}/>
            <input type="button" value="Снять выделение" onclick={this.check(this.form.list, 0)}/>
            </form>
*/