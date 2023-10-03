import './App.css';
import Chat, { Bubble, useMessages, Progress, Modal, Input } from '@chatui/core';
import '@chatui/core/dist/index.css';
import '@chatui/core/es/styles/index.less';
import React, { useEffect, useState } from 'react';
import './chatui-theme.css';
import { marked } from "marked";
import QRCode from 'react-qr-code';
import packageJson from '../package.json';
import MComposer from './MComposer';

var modelname = "ChatGLM-6b";
var history = []

const defaultQuickReplies = [
  {
    icon: 'message',
    name: 'ChatGLM2',
    isNew: false,
    isHighlight: true,
  },
  {
    icon: 'file',
    name: '通义千问',
    isNew: true,
    isHighlight: true,
  },
  {
    icon: 'keyboard-circle',
    name: '历史'
  },
  {
    icon: 'plus-circle',
    name: 'token设置'
  }
];


const initialMessages = [
  {
    type: 'text',
    content: { text: 'Aiit-Chat' },
    user: { avatar: '//gitclone.com/download1/gitclone.png' },
  }
];

function App() {
  const { messages, appendMsg, setTyping } = useMessages(initialMessages);
  const [percentage, setPercentage] = useState(0);
  const msgRef = React.useRef(null);
  const [showQRCode, setShowQRCode] = useState(false)
  const [version, setVersion] = useState("");
  const [showHistory, setShowHistory] = useState(false)
  const [showToken, setShowToken] = useState(false)
  const [token, setToken] = useState('');

  const inputRef = React.useRef(null);

  function handleSend(type, val) {
    if (percentage > 0) {
      alert("正在生成中，请稍候，或刷新页面！");
      return;
    }
    if (type === 'text' && val.trim()) {
      appendMsg({
        type: 'text',
        content: { text: val },
        position: 'right',
        user: { avatar: '//gitclone.com/download1/user.png' },
      });
      setTyping(true);
      setPercentage(10);
      onGenCode(val, 0);
    }
  }

  function renderMessageContent(msg) {
    const { type, content } = msg;

    switch (type) {
      case 'text':
        return <Bubble content={content.text} />;
      case 'image':
        return (
          <Bubble type="image">
            <img src={content.picUrl} alt="" />
          </Bubble>
        );
      default:
        return null;
    }
  }

  function setDefaultInput(val) {
    var oUl = document.getElementById('root');
    var aBox = getByClass(oUl, 'Input Input--outline Composer-input');
    if (aBox.length > 0) {
      if (inputRef && inputRef.current) {
        inputRef.current.setText(val);
      }
      aBox[0].focus();
    }
  }

  function handleQuickReplyClick(item) {
    if (item.name.startsWith("历史")) {
      setShowHistory(true);
      return;
    }
    if (item.name.startsWith("token设置")) {
      setShowToken(true);
      return;
    }
    if (item.name.startsWith("ChatGLM")) {
      modelname = "ChatGLM-6b";
      changeTitleStyle(0);
    }
    else if (item.name.startsWith("通义千问")) {
      modelname = "Qwen-7b";
      changeTitleStyle(2);
    }
    else {
      modelname = "ChatGLM-6b";
      changeTitleStyle(0);
    }
    handleSend('text', "你好");
  }

  function Sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  function markdown(code) {
    return marked(code);
  }

  async function onGenCode(prompt, count) {
    var stop = false;
    var x = 240;
    var result = "";
    await Sleep(500);
    if (count >= x) {
      setPercentage(0);
      return;
    }
    let xhr = new XMLHttpRequest();
    xhr.open('post', 'https://chat.aliendao.cn/api/stream/v2');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
      var json;
      try {
        json = JSON.parse(xhr.response);
      } catch (error) {
        updateMsg(error);
        setPercentage(0);
        return;
      }
      result = json.response;
      stop = json.stop;
      history = json.history;
      if (count === 0) {
        result = markdown(result);
        appendMsg({
          type: 'text',
          content: { text: "" },
          user: { avatar: '//gitclone.com/download1/aiit/' + modelname + '.gif' },
        });
        setTimeout(() => { updateMsg(result); }, 200);
      } else {
        if ((count > 20) && ((result === "思考中") || (result === ""))) {
          updateMsg("请更换问题或稍候再试！");
          setPercentage(0);
          return;
        }
        updateMsg(result);
      }
      count++;
      setPercentage(count * 10);
      if (stop) {
        setPercentage(0);
        return;
      }
      onGenCode(prompt, count);
    }
    //只保留5个历史对话
    if (history.length > 5) {
      history.shift();
    }
    var context = JSON.stringify({
      "context": {
        "prompt": prompt,
        "history": history
      },
      "modelname": modelname
    });
    xhr.send(context);

    function updateMsg(context) {
      context = markdown(context);
      var oUl = document.getElementById('root');
      var aBox = getByClass(oUl, 'Bubble text');
      if (aBox.length > 0) {
        aBox[aBox.length - 1].innerHTML = "<p>" + context + "</p>";
        var msgList = getByClass(oUl, "PullToRefresh")[0];
        msgList.scrollTo(0, msgList.scrollHeight);
      }
    }
  }

  function findInArr(arr, n) {
    for (var i = 0; i < arr.length; i++) {
      if (arr[i] === n) return true;
    }
    return false;
  };

  function getByClass(oParent, sClass) {
    if (document.getElementsByClassName) {
      return oParent.getElementsByClassName(sClass);
    } else {
      var aEle = oParent.getElementsByTagName('*');
      var arr = [];
      for (var i = 0; i < aEle.length; i++) {
        var tmp = aEle[i].className.split(' ');
        if (findInArr(tmp, sClass)) {
          arr.push(aEle[i]);
        }
      }
      return arr;
    }
  }

  function onRightContentClick() {
    window.open('https://github.com/git-cloner/aliendao', '_blank');
  }

  function onInputFocus(e) {
    if (msgRef && msgRef.current) {
      msgRef.current.scrollToEnd();
    }
  }

  function onLeftContentClick() {
    openQRCode();
  }

  function openQRCode() {
    setVersion(packageJson.name + ' ' + packageJson.version);
    setShowQRCode(true);
  }

  function changeTitleStyle(mode) {
    var oUl = document.getElementById('root');
    var aBox = getByClass(oUl, 'Navbar-title');
    if (aBox.length > 0) {
      if (mode === 0) {
        aBox[0].style.color = 'black';
      }
      else if (mode === 1) {
        aBox[0].style.color = 'blue';
      }
      else {
        aBox[0].style.color = 'green';
      }
    }
  }

  function handleHistoryClose() {
    setShowHistory(false);
  }

  function handleHistoryClear() {
    history = [];
    setShowHistory(false);
  }

  function handleHistoryClick(item) {
    setShowHistory(false);
    setTimeout(() => { setDefaultInput(item); }, 200);
  }


  function handleTokenClose() {
    setShowToken(false);
  }

  function handleTokenConfirm() {
    localStorage.setItem('aiit-chat-token', token);
    setShowToken(false);
  }

  useEffect(() => {
    if (showToken){
      return ;
    }
    var oUl = document.getElementById('root');
    var aBox = getByClass(oUl, 'Input Input--outline Composer-input');
    if (aBox.length > 0) {
      if (showQRCode) {
        aBox[0].blur();
      }
      else {
        aBox[0].focus();
      }
    }
    if (!showToken){
      setToken(localStorage.getItem('aiit-chat-token'));
    }
  })

  return (
    <div style={{ height: 'calc(100vh - 2px)', marginTop: '-5px' }}>
      <Chat
        navbar={{
          leftContent: {
            icon: 'apps',
            title: '关于Aiit-Chat',
            onClick: onLeftContentClick,

          },
          rightContent: [
            {
              title: '源码',
              img: '//gitclone.com/download1/aiit/github.png',
              onClick: onRightContentClick,
            },
          ],
          title: 'AIITChat(' + modelname + ')',
        }}
        messages={messages}
        messagesRef={msgRef}
        renderMessageContent={renderMessageContent}
        quickReplies={defaultQuickReplies}
        onQuickReplyClick={handleQuickReplyClick}
        onSend={handleSend}
        placeholder="shift + 回车换行，.或。提示"
        composerRef={inputRef}
        onInputFocus={onInputFocus}
        Composer={MComposer}
      />
      <Progress value={percentage} />
      {showQRCode && (
        <div className="qr-code-modal">
          <div className="qr-code-content">
            <QRCode value="https://chat.aliendao.cn/" />
            <div style={{ textAlign: 'center', marginTop: '10px' }}>
              <div>gitclone@126.com</div>
              <br></br>
              <div>{version}</div>
              <p></p>
              <button onClick={() => setShowQRCode(false)}>关闭</button>
            </div>
          </div>
        </div>
      )}
      {

        <div>
          <Modal
            active={showHistory}
            title="历史"
            showClose={false}
            onClose={handleHistoryClose}
            actions={[
              {
                label: '清除',
                color: 'primary',
                onClick: handleHistoryClear,
              },
              {
                label: '取消',
                onClick: handleHistoryClose,
              },
            ]}
            history={history}
          >
            <div style={{ overflow: 'hidden' }}>
              {
                history.map((item, index) => <div key={item[0]} style={{ paddingLeft: '15px', paddingBottom: '15px' }}
                  onClick={() => handleHistoryClick(item[0])}>{index + 1}. {item[0]}</div>)
              }
            </div>
          </Modal>
        </div>

      }
      {

        <div>
          <Modal
            active={showToken}
            title="token"
            showClose={false}
            onClose={setShowToken}
            actions={[
              {
                label: '确定',
                color: 'primary',
                onClick: handleTokenConfirm,
              },
              {
                label: '取消',
                onClick: handleTokenClose,
              },
            ]}
            children={<div style={{ overflow: 'hidden' }}>
              {
                <Input value={token} onChange={val => setToken(val)} placeholder="请输入token" />
              }
            </div>}
          >

          </Modal>
        </div>

      }
    </div>
  );
}

export default App;
