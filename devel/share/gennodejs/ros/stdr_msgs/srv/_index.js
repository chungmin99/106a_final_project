
"use strict";

let DeleteCO2Source = require('./DeleteCO2Source.js')
let DeleteRfidTag = require('./DeleteRfidTag.js')
let DeleteSoundSource = require('./DeleteSoundSource.js')
let DeleteThermalSource = require('./DeleteThermalSource.js')
let RegisterGui = require('./RegisterGui.js')
let AddThermalSource = require('./AddThermalSource.js')
let AddRfidTag = require('./AddRfidTag.js')
let AddCO2Source = require('./AddCO2Source.js')
let LoadMap = require('./LoadMap.js')
let MoveRobot = require('./MoveRobot.js')
let AddSoundSource = require('./AddSoundSource.js')
let LoadExternalMap = require('./LoadExternalMap.js')

module.exports = {
  DeleteCO2Source: DeleteCO2Source,
  DeleteRfidTag: DeleteRfidTag,
  DeleteSoundSource: DeleteSoundSource,
  DeleteThermalSource: DeleteThermalSource,
  RegisterGui: RegisterGui,
  AddThermalSource: AddThermalSource,
  AddRfidTag: AddRfidTag,
  AddCO2Source: AddCO2Source,
  LoadMap: LoadMap,
  MoveRobot: MoveRobot,
  AddSoundSource: AddSoundSource,
  LoadExternalMap: LoadExternalMap,
};
