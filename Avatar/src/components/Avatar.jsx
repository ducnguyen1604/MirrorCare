/*
Auto-generated by: https://github.com/pmndrs/gltfjsx
*/

import { useAnimations, useFBX, useGLTF } from "@react-three/drei";
import {useFrame, useLoader } from "@react-three/fiber";
import { useControls } from "leva";
import React, { useEffect, useMemo, useRef, useState } from "react";

import axios from 'axios';

import * as THREE from "three";

const corresponding = {
  A: "viseme_PP",
  B: "viseme_kk",
  C: "viseme_I",
  D: "viseme_AA",
  E: "viseme_O",
  F: "viseme_U",
  G: "viseme_FF",
  H: "viseme_TH",
  X: "viseme_PP",
};

export function Avatar(props) {
  const [data, setData] = useState({});

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/get_data');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };


  const {playAudio, script} = useControls({
    playAudio: false,
    script: {
      value: "output_speech",
      options: ["output_speech", "welcome"],
    }
  });

  const audio = useMemo(() => new Audio(`/audios/${script}.mp3`), [script]);
  const jsonFile = useLoader(THREE.FileLoader, `audios/${script}.json`);
  const lipsync = JSON.parse(jsonFile);

  useFrame(() => {
    const currentAudioTime = audio.currentTime;
    if (audio.paused || audio.ended) {
      setAnimation("Idle");
    }

    Object.values(corresponding).forEach((value) => {
      nodes.Wolf3D_Head.morphTargetInfluences[
        nodes.Wolf3D_Head.morphTargetDictionary[value]
      ] = 0;
      nodes.Wolf3D_Teeth.morphTargetInfluences[
        nodes.Wolf3D_Teeth.morphTargetDictionary[value]
      ] = 0;
    });

    for (let i = 0; i< lipsync.mouthCues.length; i++){
      const mouthCue = lipsync.mouthCues[i];
      if (
        currentAudioTime >= mouthCue.start && 
        currentAudioTime <= mouthCue.end
      ) {
        console.log(mouthCue.value);
        nodes.Wolf3D_Head.morphTargetInfluences[
          nodes.Wolf3D_Head.morphTargetDictionary[corresponding[mouthCue.value]]
        ] = 1;
        nodes.Wolf3D_Teeth.morphTargetInfluences[
          nodes.Wolf3D_Teeth.morphTargetDictionary[
            corresponding[mouthCue.value]
          ]
        ] = 1;
        break;
      }
    }
  })


  useEffect(() => {
    if (JSON.stringify(data) === "true") {
      console.log(JSON.stringify(data) === "true")

      audio.play();
      if (script === "welcome") {
        setAnimation("Wave");
      } else if (script === "output_speech") {
        setAnimation("Happy");
      } else {
        setAnimation("Idle");
      }
    } else{
      setAnimation("Idle");
      audio.pause();
    }
    const intervalId = setInterval(fetchData, 5000);
    return () => clearInterval(intervalId);

  }, [data, playAudio, script]);

  const { nodes, materials } = useGLTF("/models/65e5a50231e5a611a0c83daf.glb");
  const { animations: idleAnimation } = useFBX(
    "/animations/Idle.fbx"
  );
  const { animations: happyAnimation } = useFBX(
    "/animations/Happy.fbx"
  );
  const { animations: waveAnimation } = useFBX(
    "/animations/Wave.fbx"
  );
  const { animations: thinkAnimation } = useFBX(
    "/animations/Think.fbx"
  );

  idleAnimation[0].name = "Idle";
  happyAnimation[0].name = "Happy";
  waveAnimation[0].name = "Wave";
  thinkAnimation[0].name = "Think";


  const [animation, setAnimation] = useState("Idle");

  const group = useRef();
  const { actions } = useAnimations(
    [idleAnimation[0], happyAnimation[0], waveAnimation[0], thinkAnimation[0]], 
    group
  );

  useEffect(() => {
    actions[animation].reset().fadeIn(0.5).play();
    return () => actions[animation].fadeOut(0.5);
  }, [animation]);

  return (
    <group {...props} dispose={null} ref={group}>
      <primitive object={nodes.Hips} />
      <skinnedMesh
        name="EyeLeft"
        geometry={nodes.EyeLeft.geometry}
        material={materials.Wolf3D_Eye}
        skeleton={nodes.EyeLeft.skeleton}
        morphTargetDictionary={nodes.EyeLeft.morphTargetDictionary}
        morphTargetInfluences={nodes.EyeLeft.morphTargetInfluences}
      />
      <skinnedMesh
        name="EyeRight"
        geometry={nodes.EyeRight.geometry}
        material={materials.Wolf3D_Eye}
        skeleton={nodes.EyeRight.skeleton}
        morphTargetDictionary={nodes.EyeRight.morphTargetDictionary}
        morphTargetInfluences={nodes.EyeRight.morphTargetInfluences}
      />
      <skinnedMesh
        name="Wolf3D_Head"
        geometry={nodes.Wolf3D_Head.geometry}
        material={materials.Wolf3D_Skin}
        skeleton={nodes.Wolf3D_Head.skeleton}
        morphTargetDictionary={nodes.Wolf3D_Head.morphTargetDictionary}
        morphTargetInfluences={nodes.Wolf3D_Head.morphTargetInfluences}
      />
      <skinnedMesh
        name="Wolf3D_Teeth"
        geometry={nodes.Wolf3D_Teeth.geometry}
        material={materials.Wolf3D_Teeth}
        skeleton={nodes.Wolf3D_Teeth.skeleton}
        morphTargetDictionary={nodes.Wolf3D_Teeth.morphTargetDictionary}
        morphTargetInfluences={nodes.Wolf3D_Teeth.morphTargetInfluences}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Hair.geometry}
        material={materials.Wolf3D_Hair}
        skeleton={nodes.Wolf3D_Hair.skeleton}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Body.geometry}
        material={materials.Wolf3D_Body}
        skeleton={nodes.Wolf3D_Body.skeleton}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Outfit_Bottom.geometry}
        material={materials.Wolf3D_Outfit_Bottom}
        skeleton={nodes.Wolf3D_Outfit_Bottom.skeleton}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Outfit_Footwear.geometry}
        material={materials.Wolf3D_Outfit_Footwear}
        skeleton={nodes.Wolf3D_Outfit_Footwear.skeleton}
      />
      <skinnedMesh
        geometry={nodes.Wolf3D_Outfit_Top.geometry}
        material={materials.Wolf3D_Outfit_Top}
        skeleton={nodes.Wolf3D_Outfit_Top.skeleton}
      />
    </group>
  );
}

useGLTF.preload("/models/65e5a50231e5a611a0c83daf.glb");