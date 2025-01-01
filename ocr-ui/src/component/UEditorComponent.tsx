import React, { useRef, useEffect, useState } from 'react';

const UEditorComponent = ({ id, value, onChange }) => {
  const editorRef = useRef(null);
  const [editorInstance, setEditorInstance] = useState(null);
  let bool = false
  useEffect(() => {
    if (typeof window.UE !== 'undefined') {
      bool = false
      const editor = window.UE.getEditor(id, {
        initialFrameWidth: null,
        initialFrameHeight: 350,
      });
      setEditorInstance(editor);
      editor.ready(function() {
        bool = true
        editor.setContent(value,true);
      });
      // 设置初始内容
      // if (value) {
      //   setTimeout(() => {
      //     editor.setContent(value);
      //   }, 2000)
      // }

      // 监听内容变化
      editor.addListener('contentChange', () => {
        if (onChange) {
          onChange(editor.getContent());
        }
      });

      // 清理编辑器实例
      return () => {
        if (editorInstance) {
          editorInstance.destroy();
          setEditorInstance(null);
        }
      };
    }
  }, [id, value, onChange]);

  useEffect(() => {
    if (editorInstance && value && bool) {
      console.log(document.getElementById('ooooo'))
      editorInstance.setContent(value);
    }
  }, [value, editorInstance]);

  return (
    <div>
      <script id={id} type="text/plain"></script>
    </div>
  );
};

export default UEditorComponent;