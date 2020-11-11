
"use strict";

let DeleteCO2Source = require('./DeleteCO2Source.js')
let LoadExternalMap = require('./LoadExternalMap.js')
let AddCO2Source = require('./AddCO2Source.js')
let DeleteSoundSource = require('./DeleteSoundSource.js')
let RegisterGui = require('./RegisterGui.js')
let LoadMap = require('./LoadMap.js')
let AddThermalSource = require('./AddThermalSource.js')
let AddSoundSource = require('./AddSoundSource.js')
let DeleteThermalSource = require('./DeleteThermalSource.js')
let AddRfidTag = require('./AddRfidTag.js')
let MoveRobot = require('./MoveRobot.js')
let DeleteRfidTag = require('./DeleteRfidTag.js')

module.exports = {
  DeleteCO2Source: DeleteCO2Source,
  LoadExternalMap: LoadExternalMap,
  AddCO2Source: AddCO2Source,
  DeleteSoundSource: DeleteSoundSource,
  RegisterGui: RegisterGui,
  LoadMap: LoadMap,
  AddThermalSource: AddThermalSource,
  AddSoundSource: AddSoundSource,
  DeleteThermalSource: DeleteThermalSource,
  AddRfidTag: AddRfidTag,
  MoveRobot: MoveRobot,
  DeleteRfidTag: DeleteRfidTag,
};
