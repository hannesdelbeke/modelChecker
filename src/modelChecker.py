''' -------------------------- modelChecker --------------------------------

    Reliable production ready sanity checker for Autodesk Maya
    Sanity check polygon models in Autodesk Maya, and prepare
    your digital assets for a smooth sailing through the production pipeline.
    Contact: jakobjk@gmail.com
    Website: https://github.com/JakobJK/modelChecker

    ------------------------------------------------------------------------
'''

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
from functools import partial
from datetime import datetime

import sys
import os
import socket
import getpass
import codecs

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om


# GENERAL VARS
version = '0.1.2'
winWidth = 694
winHeight = 900
reportWidth = 200

sceneFullPath = cmds.file(q=True, sn=True)
sceneName = os.path.basename(sceneFullPath)
scenePath = os.path.dirname(sceneFullPath) + '/'
username = str(getpass.getuser())
hostname = str(socket.gethostname())
homedir = os.environ['HOME']
pyFilePath = os.path.dirname(os.path.abspath(__file__))




##############
#   FIXERS   #
##############

# the fix functions needs to go here eventually
# Example:
# def shapeNames_fix():

# NAMING FIXERS
undefined = 'is currently unavailable.'

def trailingNumbers_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def duplicatedNames_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def shapeNames_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    shapeNames = []
    for obj in nodes:
        new = obj.split('|')
        shape = cmds.listRelatives(obj, shapes = True)
        if shape is not None:
            name = new[-1] + 'Shape'
            if not shape[0] == name:
                cmds.rename(obj, obj+'__tmp__')
                cmds.rename(obj+'__tmp__', obj)
                cmds.select(d=True)
                fixed = 1
    
    if fixed == 1:       
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Renamed shape names! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Not renamed shape names <font color=#9c4f4f> [ FAILED ] <br>')


def namespaces_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    namespaces = []
    for obj in nodes:
        new = obj.split(':')
        namespace = new[0]
        cmds.rename(obj, new[1])
        fixed = 1

    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Removed namespaces! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Not removed namespaces <font color=#9c4f4f> [ FAILED ] <br>')


    

# TOPOLOGY FIXERS
def triangles_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def ngons_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def openEdges_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def poles_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def hardEdges_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def lamina_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def zeroAreaFaces_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def zeroLengthEdges_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def noneManifoldEdges_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def starlike_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')


# UV FIXERS

def selfPenetratingUVs_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def missingUVs_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def uvRange_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def crossBorder_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')


# GENERAL FIXERS

def layers_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    defaultLayer = ['defaultLayer']
    userLayers = []
    userLayers = cmds.ls(type = 'displayLayer')
    # Get only user layers
    dispLayers = set(userLayers).difference(set(defaultLayer))   
    for layer in dispLayers:
        cmds.delete(layer)
        fixed = 1

    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Deleted all display layers! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Error removing display layers <font color=#9c4f4f> [ FAILED ] <br>')


def history_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    cmds.select(nodes)
    for obj in nodes:
        # Delete history in selected items 
        cmds.delete(obj, ch=True) 
        fixed = 1
    # Deselect all
    cmds.select(d=True)

    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Deleted construction history! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Error removing history <font color=#9c4f4f> [ FAILED ] <br>')


def shaders_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')


def unfrozenTransforms_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    cmds.select(nodes)
    for obj in nodes:
        #Freeze all transformations
        cmds.makeIdentity(obj, apply=True, t=True, r=True, s=True, n=False)
        fixed = 1
    # Deselect all
    cmds.select(d=True)
    
    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Freeze transformations done! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Error freezing transforms <font color=#9c4f4f> [ FAILED ] <br>')


def uncenteredPivots_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    cmds.select(nodes)
    for obj in nodes:
        #Set pivot to world origin (0,0,0)
        cmds.xform(obj, a=True, piv=[0,0,0])
        fixed = 1
    # Deselect all
    cmds.select(d=True)
    
    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Pivots reseted to 0,0,0! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Error reseting pivots <font color=#9c4f4f> [ FAILED ] <br>')

    
def parentGeometry_fix(self, nodes, func_name, func_name_fix):
    self.reportOutputUI.insertHtml('<br> <font color=#c99936>' + func_name_fix + '</font> ' + undefined + '<br>')

def emptyGroups_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    emptyGroups = []
    for obj in nodes:
        children = cmds.listRelatives(obj, ad = True)
        if children is None:
            cmds.delete(obj)
            fixed = 1
    
    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Deleted all empty groups in scene! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Error removing empty groups <font color=#9c4f4f> [ FAILED ] <br>')


def selectionSets_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    selectionSets = nodes
    for sel in selectionSets:
        #Remove user sets
        cmds.delete(sel)
        fixed = 1
        
    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Deleted all userSets in scene! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Error removing user selection sets <font color=#9c4f4f> [ FAILED ] <br>')
    

def nodesInTabs_fix(self, nodes, func_name, func_name_fix):
    fixed = 0
    panels = cmds.getPanel(sty='nodeEditorPanel')

    for mypanel in panels:
        #Open window
        cmds.scriptedPanel(mypanel, e=True, to=True)
    
        ned = mypanel + 'NodeEditorEd'            
        
        #Close all tabs
        cmds.nodeEditor(ned, e=True, closeAllTabs=True)
        
        #Close window
        control = cmds.control(ned, query=True, fullPathName=True)
        cmds.deleteUI(control.split('|')[0], window=True)
        fixed = 1
    cmds.refresh()
    
    if fixed == 1:
        #Output message and restore state buttons
        self.reportOutputUI.insertHtml('<br> Cleaned all nodes in Node Editor! <font color=#3da94d> [ SUCCESS ] <br>' )
        restoreStateButtons(self, func_name)
    else:
        self.reportOutputUI.insertHtml('Error cleaning nodes in Node Editor <font color=#9c4f4f> [ FAILED ] <br>')


#Function for restoring state buttons after fix
def restoreStateButtons(self, func_name):
    self.commandLabel[func_name].setStyleSheet('background-color: none;')
    self.errorNodesButton[func_name].setEnabled(False)
    self.commandFixButton[func_name].setEnabled(False)



##############
#   CHECKS   #
##############

# NAMING CHECKS

def trailingNumbers(self, list):
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    trailingNumbers = []
    for obj in list:
        if obj[len(obj)-1] in numbers:
            trailingNumbers.append(obj)
    return trailingNumbers

def duplicatedNames(self, list):
    duplicatedNames = []
    for item in list:
    	if '|' in item:
            duplicatedNames.append(item)
    return duplicatedNames

def namespaces(self, list):
    namespaces = []
    for obj in list:
        if ':' in obj:
            namespaces.append(obj)
    return namespaces

def shapeNames(self, list):
    shapeNames = []
    for obj in list:
        new = obj.split('|')
        shape = cmds.listRelatives(obj, shapes = True)
        if shape is not None:
            name = new[-1] + 'Shape'
            if not shape[0] == name:
                shapeNames.append(obj)
    return shapeNames



# TOPOLOGY CHECKS

def triangles(self, list):
    triangles = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
    	faceIt = om.MItMeshPolygon(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not faceIt.isDone():
    	    numOfEdges = faceIt.getEdges()
    	    if len(numOfEdges) == 3:
    	        faceIndex = faceIt.index()
    	        componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
    	        triangles.append(componentName)
    	    else:
    	        pass
    	    faceIt.next(None)
    	selIt.next()
    return triangles

def ngons(self, list):
    ngons = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
    	faceIt = om.MItMeshPolygon(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not faceIt.isDone():
    	    numOfEdges = faceIt.getEdges()
    	    if len(numOfEdges) > 4:
    	        faceIndex = faceIt.index()
    	        componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
    	        ngons.append(componentName)
    	    else:
    	        pass
    	    faceIt.next(None)
    	selIt.next()
    return ngons

def hardEdges(self, list):
    hardEdges = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.isSmooth == False and edgeIt.onBoundary() == False:
                edgeIndex = edgeIt.index()
                componentName = str(objectName) + '.e[' + str(edgeIndex) + ']'
                hardEdges.append(componentName)
            else:
                pass
            edgeIt.next()
        selIt.next()
    return hardEdges

def lamina(self, list):
    selIt = om.MItSelectionList(self.SLMesh)
    lamina = []
    while not selIt.isDone():
    	faceIt = om.MItMeshPolygon(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not faceIt.isDone():
    	    laminaFaces = faceIt.isLamina()
    	    if laminaFaces == True:
    	        faceIndex = faceIt.index()
    	        componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
    	        lamina.append(componentName)
    	    else:
    	        pass
    	    faceIt.next(None)
    	selIt.next()
    return lamina

def zeroAreaFaces(self, list):
    zeroAreaFaces = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
    	faceIt = om.MItMeshPolygon(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not faceIt.isDone():
    	    faceArea = faceIt.getArea()
    	    if faceArea < 0.000001:
    	        faceIndex = faceIt.index()
    	        componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
    	        zeroAreaFaces.append(componentName)
    	    else:
    	        pass
    	    faceIt.next(None)
    	selIt.next()
    return zeroAreaFaces

def zeroLengthEdges(self, list):
    zeroLengthEdges = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
    	edgeIt = om.MItMeshEdge(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not edgeIt.isDone():
    	    if edgeIt.length() < 0.00000001:
    	        componentName = str(objectName) + '.f[' + str(edgeIt.index()) + ']'
    	        zeroLengthEdges.append(componentName)
    	    edgeIt.next()
    	selIt.next()
    return zeroLengthEdges

def selfPenetratingUVs(self, list):
    selfPenetratingUVs = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes = True, fullPath = True)
        convertToFaces = cmds.ls(cmds.polyListComponentConversion(shape, tf=True), fl=True)
        overlapping = (cmds.polyUVOverlap(convertToFaces, oc=True ))
        if overlapping is not None:
            for obj in overlapping:
                selfPenetratingUVs.append(obj)
    return selfPenetratingUVs

def noneManifoldEdges(self, list):
    noneManifoldEdges = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() > 2:
                edgeIndex = edgeIt.index()
                componentName = str(objectName) + '.e[' + str(edgeIndex) + ']'
                noneManifoldEdges.append(componentName)
            else:
                pass
            edgeIt.next()
        selIt.next()
    return noneManifoldEdges

def openEdges(self, list):
    openEdges = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() < 2:
                edgeIndex = edgeIt.index()
                componentName = str(objectName) + '.e[' + str(edgeIndex) + ']'
                openEdges.append(componentName)
            else:
                pass
            edgeIt.next()
        selIt.next()
    return openEdges

def poles(self, list):
    poles = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
        vertexIt = om.MItMeshVertex(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not vertexIt.isDone():
            if vertexIt.numConnectedEdges() > 5:
                vertexIndex = vertexIt.index()
                componentName = str(objectName) + '.vtx[' + str(vertexIndex) + ']'
                poles.append(componentName)
            else:
                pass
            vertexIt.next()
        selIt.next()
    return poles

def starlike(self, list):
    starlike = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
        polyIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not polyIt.isDone():
            if polyIt.isStarlike() == False:
                polygonIndex = polyIt.index()
                componentName = str(objectName) + '.e[' + str(polygonIndex) + ']'
                starlike.append(componentName)
            else:
                pass
            polyIt.next(None)
        selIt.next()
    return starlike


# UV CHECKS

def missingUVs(self, list):
    missingUVs = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
    	faceIt = om.MItMeshPolygon(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not faceIt.isDone():
            if faceIt.hasUVs() == False:
                componentName = str(objectName) + '.f[' + str(faceIt.index()) + ']'
                missingUVs.append(componentName)
    	    faceIt.next(None)
    	selIt.next()
    return missingUVs


def uvRange(self, list):
    uvRange = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
    	faceIt = om.MItMeshPolygon(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not faceIt.isDone():
            UVs = faceIt.getUVs()
            for index, eachUVs in enumerate(UVs):
                if index == 0:
                    for eachUV in eachUVs:
                        if eachUV < 0 or eachUV > 10:
                            componentName = str(objectName) + '.f[' + str(faceIt.index()) + ']'
                            uvRange.append(componentName)
                            break
                if index == 1:
                    for eachUV in eachUVs:
                        if eachUV < 0:
                            componentName = str(objectName) + '.f[' + str(faceIt.index()) + ']'
                            uvRange.append(componentName)
                            break
    	    faceIt.next(None)
    	selIt.next()
    return uvRange

def crossBorder(self, list):
    crossBorder = []
    selIt = om.MItSelectionList(self.SLMesh)
    while not selIt.isDone():
    	faceIt = om.MItMeshPolygon(selIt.getDagPath())
    	objectName = selIt.getDagPath().getPath()
    	while not faceIt.isDone():
            U = None
            V = None
            UVs = faceIt.getUVs()
            for index, eachUVs in enumerate(UVs):
                if index == 0:
                    for eachUV in eachUVs:
                        if U == None:
                            U = int(eachUV)
                        if U != int(eachUV):
                            componentName = str(objectName) + '.f[' + str(faceIt.index()) + ']'
                            crossBorder.append(componentName)
                if index == 1:
                    for eachUV in eachUVs:
                        if V == None:
                            V = int(eachUV)
                        if V != int(eachUV):
                            componentName = str(objectName) + '.f[' + str(faceIt.index()) + ']'
                            crossBorder.append(componentName)
    	    faceIt.next(None)
    	selIt.next()
    return crossBorder


# GENERAL CHECKS

def unfrozenTransforms(self, list):
    unfrozenTransforms = []
    for obj in list:
        translation = cmds.xform(obj, q=True, worldSpace = True, translation = True)
        rotation = cmds.xform(obj, q=True, worldSpace = True, rotation = True)
        scale = cmds.xform(obj, q=True, worldSpace = True, scale = True)
        if not translation == [0.0,0.0,0.0] or not rotation == [0.0,0.0,0.0] or not scale == [1.0,1.0,1.0]:
            unfrozenTransforms.append(obj)
    return unfrozenTransforms

def layers(self, list):
    defaultLayer = ['defaultLayer']
    userLayers = []
    userLayers = cmds.ls(type = 'displayLayer')
    # Get only user layers
    dispLayers = set(userLayers).difference(set(defaultLayer))    
    layers = dispLayers
    return layers

def shaders(self, list):
    shaders = []
    for obj in list:
        shadingGrps = None
        shape = cmds.listRelatives(obj, shapes = True, fullPath = True)
        if cmds.nodeType(shape) == 'mesh':
            if shape is not None:
                shadingGrps = cmds.listConnections(shape, type='shadingEngine')
            if not shadingGrps[0] == 'initialShadingGroup':
                shaders.append(obj)
    return shaders

def history(self, list):
    history = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes = True, fullPath = True)
        if shape is not None:
            if cmds.nodeType(shape[0]) == 'mesh':
                historySize = len(cmds.listHistory(shape))
                if historySize > 1:
                    history.append(obj)
    return history

def uncenteredPivots(self, list):
    uncenteredPivots = []
    for obj in list:
        if cmds.xform(obj,q=1,ws=1,rp=1) != [0,0,0]:
            uncenteredPivots.append(obj)
    return uncenteredPivots

def parentGeometry(self, list):
    parentGeometry = []
    shapeNode = False
    for obj in list:
        shapeNode = False
        parents = cmds.listRelatives(obj, p = True, fullPath = True)
        if parents is not None:
            for i in parents:
                parentsChildren = cmds.listRelatives(i, fullPath = True)
                for l in parentsChildren:
                    if cmds.nodeType(l) == 'mesh':
                        shapeNode = True
        if shapeNode == True:
            parentGeometry.append(obj)
    return parentGeometry

def emptyGroups(self, list):
    emptyGroups = []
    for obj in list:
        children = cmds.listRelatives(obj, ad = True)
        if children is None:
            emptyGroups.append(obj)
    return emptyGroups

def selectionSets(self, list):
    # Create list getting all sets in scene
    allSets = cmds.listSets( allSets=True )

    # Create list with all isolation sets
    isolationSets = []
    for n in range(10):
        isolationSets.append('modelPanel' + str(n) + 'ViewSelectedSet')
    
    # Check if any isolation set exists 
    result = any(elem in allSets for elem in isolationSets)

    if result:
        self.reportOutputUI.insertHtml('<br>You must exit of isolated mode for any object <font color=#9c4f4f> [ FAILED ] <br>')
        return selectionSets
    else:
        # Create list with all default sets
        defaultSets = [ 'defaultLastHiddenSet',
                        'defaultHideFaceDataSet', 
                        'defaultCreaseDataSet'
                        'defaultObjectSet',
                        'defaultLightSet',
                        'internal_standInSE',
                        'internal_soloSE',
                        'initialParticleSE',
                        'initialShadingGroup',
                        'defaultObjectSet',
                        'defaultCreaseDataSet'
                    ]
        # Get user sets from difference between both lists
        userSets = set(allSets).difference(set(defaultSets)) 
        
        selectionSets = userSets
        return selectionSets


def nodesInTabs(self, list):
    nodesInTabs = []
    outNodes = False
    for obj in list:
        outNodes = False
        objects = cmds.listConnections(obj, d=True, s=False)
        if objects is not None:
            for outNodes in objects:
                if 'MayaNodeEditorSavedTabsInfo' in outNodes:
                    outNodes = True
        if outNodes == True:
            nodesInTabs.append(obj)
    return nodesInTabs




###################
#   UI BUILDING   #
###################

def getMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    return mainWindow

class modelChecker(QtWidgets.QMainWindow):

    def __init__(self, parent=getMainWindow()):
        super(modelChecker, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)

        # Creates object, Title Name and Adds a QtWidget as our central widget/Main Layout
        self.setObjectName('modelCheckerUI')
        self.setWindowTitle('Model Checker' + ' ' + 'v' + version)
        mainLayout = QtWidgets.QWidget(self)
        self.setCentralWidget(mainLayout)

        # Adding a Horizontal layout to divide the UI in two columns
        columns = QtWidgets.QHBoxLayout(mainLayout)

        # Creating 2 vertical layout for the sanity checks and one for the report
        self.report = QtWidgets.QVBoxLayout()
        self.checks = QtWidgets.QVBoxLayout()

        # Set columns for each layout using stretch policy to psudo fixed width for the 'checks' layout
        columns.addLayout(self.checks, 1)
        columns.addLayout(self.report, 99)


        # Adding UI ELEMENTS FOR CHECKS
        selectedModelVLayout = QtWidgets.QHBoxLayout()
        self.checks.addLayout(selectedModelVLayout)

        selectedModelLabel = QtWidgets.QLabel('Top Node')
        selectedModelLabel.setFixedWidth(60)

        self.selectedTopNode_UI = QtWidgets.QLineEdit('')
        self.selectedTopNode_UI.setMinimumWidth(270)

        self.selectedModelNodeButton = QtWidgets.QPushButton('Select')
        self.selectedModelNodeButton.setFixedWidth(65)
        self.selectedModelNodeButton.clicked.connect(self.setTopNode)

        selectedModelVLayout.addWidget(selectedModelLabel)
        selectedModelVLayout.addWidget(self.selectedTopNode_UI)
        selectedModelVLayout.addWidget(self.selectedModelNodeButton)


        # Adding UI elements to the repport
        self.toolbarLayout = QtWidgets.QHBoxLayout()
        self.report.addLayout(self.toolbarLayout)

        self.reportBoxLayout = QtWidgets.QHBoxLayout()
        self.report.addLayout(self.reportBoxLayout)

        self.reportButtonsLayout = QtWidgets.QHBoxLayout()
        self.report.addLayout(self.reportButtonsLayout)

        self.reportOutputUI = QtWidgets.QTextEdit()
        self.reportOutputUI.setMinimumWidth(reportWidth)

        self.aboutButton = QtWidgets.QPushButton()
        self.aboutButton.setFlat(True)
        self.aboutButton.setIcon(QtGui.QIcon(pyFilePath + '/modelChecker_icon.png'))
        self.aboutButton.setIconSize(QtCore.QSize(32,32))
        self.aboutButton.clicked.connect(partial(self.aboutText))

        reportLabel = QtWidgets.QLabel('Report:')
        reportLabel.setMaximumWidth(40)

        self.clearButton = QtWidgets.QPushButton('Clear')
        self.clearButton.setMinimumWidth(60)
        self.clearButton.clicked.connect(partial(self.reportOutputUI.clear))

        self.saveButton = QtWidgets.QPushButton('Save')
        self.saveButton.setMinimumWidth(60)
        self.saveButton.clicked.connect(partial(self.saveReport))

        self.toolbarLayout.addWidget(self.aboutButton, 0, QtCore.Qt.AlignRight)
        self.reportBoxLayout.addWidget(self.reportOutputUI)
        self.reportButtonsLayout.addWidget(reportLabel, 0, QtCore.Qt.AlignLeft)
        self.reportButtonsLayout.addWidget(self.clearButton, 1, QtCore.Qt.AlignRight)
        self.reportButtonsLayout.addWidget(self.saveButton, 0, QtCore.Qt.AlignRight)
        

        # Adding the stretch element to the checks UI to get everything at the top
        self.resize(winWidth,winHeight)
        self.list = [
                'trailingNumbers_naming_1_0',
                'duplicatedNames_naming_1_0',
                'shapeNames_naming_1_0',
                'namespaces_naming_1_0',

                'layers_general_1_0',
                'history_general_1_0',
                'shaders_general_1_0',
                'unfrozenTransforms_general_1_0',
                'uncenteredPivots_general_1_0',
                'parentGeometry_general_1_0',
                'emptyGroups_general_1_0',
                'selectionSets_general_1_0',
                'nodesInTabs_general_1_0',

                'triangles_topology_0_0',
                'ngons_topology_0_0',
                'openEdges_topology_0_0',
                'poles_topology_0_0',
                'hardEdges_topology_0_0',
                'lamina_topology_0_0',
                'zeroAreaFaces_topology_0_0',
                'zeroLengthEdges_topology_0_0',
                'noneManifoldEdges_topology_0_0',
                'starlike_topology_0_0',

                'selfPenetratingUVs_UVs_0_0',
                'missingUVs_UVs_0_0',
                'uvRange_UVs_0_0',
                'crossBorder_UVs_0_0'
                ]

        allCategories = []

        for obj in self.list:
            number = obj.split('_')
            allCategories.append(number[1])

        category = set(allCategories)
        self.SLMesh = om.MSelectionList()

        self.categoryLayout = {}
        self.categoryWidget = {}
        self.categoryButton = {}
        self.categoryHeader = {}
        self.categoryCollapse = {}
        self.command = {}
        self.commandWidget = {}
        self.commandLayout = {}
        self.commandInfo = {}
        self.commandLabel = {}
        self.commandCheckBox = {}
        self.errorNodesButton = {}
        self.commandFixButton = {}
        self.commandFix = {}
        self.commandRunButton = {}

        # Create the Categories section!!
        for obj in category:
            self.categoryWidget[obj] = QtWidgets.QWidget()
            self.categoryLayout[obj] = QtWidgets.QVBoxLayout()
            self.categoryHeader[obj] = QtWidgets.QHBoxLayout()
            self.categoryButton[obj] = QtWidgets.QPushButton(obj)
            self.categoryCollapse[obj] = QtWidgets.QPushButton(u'\u2193'.encode('utf-8'))
            self.categoryCollapse[obj].clicked.connect(partial(self.toggleUI, obj))
            self.categoryCollapse[obj].setMaximumWidth(30)
            self.categoryButton[obj].setStyleSheet('background-color: #777; text-transform: uppercase; color: #CCC; font-size: 11px;')
            self.categoryButton[obj].clicked.connect(partial(self.checkCategory, obj))
            self.categoryHeader[obj].addWidget(self.categoryButton[obj])
            self.categoryHeader[obj].addWidget(self.categoryCollapse[obj])
            self.categoryWidget[obj].setLayout(self.categoryLayout[obj])
            self.checks.addLayout(self.categoryHeader[obj])
            self.checks.addWidget(self.categoryWidget[obj])

        # Creates the buttons with their settings.
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            category = new[1]
            check = int(new[2])
            fix = int(new[3])

            self.commandWidget[name] = QtWidgets.QWidget()
            self.commandWidget[name].setMaximumHeight(40)
            self.commandLayout[name] = QtWidgets.QHBoxLayout()

            self.categoryLayout[category].addWidget(self.commandWidget[name])
            self.commandWidget[name].setLayout(self.commandLayout[name])

            self.commandLayout[name].setSpacing(4)
            self.commandLayout[name].setContentsMargins(0,0,0,0)
            self.commandWidget[name].setStyleSheet('padding: 0px; margin: 0px;')
            
            self.command[name] = name
            
            self.commandInfo[name] = QtWidgets.QPushButton(u'\u24d8')
            self.commandInfo[name].setStyleSheet('color: #222;')
            self.commandInfo[name].setFixedWidth(18)
            self.commandInfo[name].setFlat(True)
            self.commandInfo[name].clicked.connect(partial(self.getInfo, [eval(name)] ))

            self.commandLabel[name] = QtWidgets.QLabel(name)
            self.commandLabel[name].setFixedWidth(150)

            self.commandCheckBox[name] = QtWidgets.QCheckBox()
            self.commandCheckBox[name].setChecked(check)
            self.commandCheckBox[name].setMaximumWidth(20)

            self.commandRunButton[name] = QtWidgets.QPushButton('Run')
            self.commandRunButton[name].setFixedWidth(40)
            self.commandRunButton[name].clicked.connect(partial(self.commandToRun, [eval(name)]))

            self.errorNodesButton[name] = QtWidgets.QPushButton('Select Error Nodes')
            self.errorNodesButton[name].setEnabled(False)
            self.errorNodesButton[name].setFixedWidth(110)

            self.commandFixButton[name] = QtWidgets.QPushButton('Fix')
            self.commandFixButton[name].setEnabled(False)
            self.commandFixButton[name].setFixedWidth(30)
           
            self.commandLayout[name].addWidget(self.commandInfo[name])
            self.commandLayout[name].addWidget(self.commandLabel[name])
            self.commandLayout[name].addWidget(self.commandCheckBox[name])
            self.commandLayout[name].addWidget(self.commandRunButton[name])
            self.commandLayout[name].addWidget(self.errorNodesButton[name])
            self.commandLayout[name].addWidget(self.commandFixButton[name])

        self.checks.addStretch()

        self.checkButtonsLayout = QtWidgets.QHBoxLayout()
        self.checks.addLayout(self.checkButtonsLayout)

        self.bottomButtonsLayout = QtWidgets.QHBoxLayout()
        self.checks.addLayout(self.bottomButtonsLayout)

        self.restoreButton = QtWidgets.QPushButton('Reset UI')
        self.restoreButton.setMaximumWidth(60)
        self.restoreButton.clicked.connect(self.restoreState)
        
        checkLabel = QtWidgets.QLabel('Check:')

        self.checkAllButton = QtWidgets.QPushButton('All')
        self.checkAllButton.setFixedWidth(45)
        self.checkAllButton.clicked.connect(self.checkAll)

        self.uncheckAllButton = QtWidgets.QPushButton('None')
        self.uncheckAllButton.setFixedWidth(45)
        self.uncheckAllButton.clicked.connect(self.uncheckAll)

        self.invertCheckButton = QtWidgets.QPushButton('Invert')
        self.invertCheckButton.setFixedWidth(45)
        self.invertCheckButton.clicked.connect(self.invertCheck)
        
        self.checkRunButton = QtWidgets.QPushButton('Run All Checked')
        #self.checkRunButton.setFixedWidth(204)
        self.checkRunButton.setStyleSheet('background-color: #58636b;')
        self.checkRunButton.clicked.connect(self.sanityCheck)
        
        self.checkButtonsLayout.addWidget(checkLabel)
        self.checkButtonsLayout.addWidget(self.checkAllButton)
        self.checkButtonsLayout.addWidget(self.uncheckAllButton)
        self.checkButtonsLayout.addWidget(self.invertCheckButton, 1, QtCore.Qt.AlignLeft)
        self.checkButtonsLayout.addWidget(self.restoreButton, 0, QtCore.Qt.AlignRight)
        self.bottomButtonsLayout.addWidget(self.checkRunButton)






#################
#  UI MANAGING  #
#################

    # Definitions to manipulate the UI
    def setTopNode(self):
        sel = cmds.ls(selection = True)
        self.selectedTopNode_UI.setText(sel[0])


    # Checks the state of a given checkbox
    def checkState(self, name):
        return self.commandCheckBox[name].checkState()


    # Sets all checkboxes to True
    def checkAll(self):
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            self.commandCheckBox[name].setChecked(True)


    def toggleUI(self, obj):
       state = self.categoryWidget[obj].isVisible()
       if state:
           self.categoryCollapse[obj].setText(u'\u21B5'.encode('utf-8'))
           self.categoryWidget[obj].setVisible(not state)
           self.adjustSize()
       else:
           self.categoryCollapse[obj].setText(u'\u2193'.encode('utf-8'))
           self.categoryWidget[obj].setVisible(not state)


    # Sets all checkboxes to False
    def uncheckAll(self):
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            self.commandCheckBox[name].setChecked(False)


    # Sets the checkbox to the oppositve of current state
    def invertCheck(self):
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            self.commandCheckBox[name].setChecked(not self.commandCheckBox[name].isChecked())


    # Restore state button labels and clear report UI
    def restoreState(self):
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            self.commandLabel[name].setStyleSheet('background-color: none;')
            self.errorNodesButton[name].setEnabled(False)
            self.commandFixButton[name].setEnabled(False)        
        self.reportOutputUI.clear()

    
    # Content for about
    def aboutText(self):
        self.reportOutputUI.clear()
        self.reportOutputUI.insertHtml( '<br>' 
                                        '<b>Usage</b><p>'
                                        'There are three ways to run the checks.<ol>'
                                        '<li>If you have objects selected the checks will run on the current selection.</li><br>'
                                        '<li>A hierachy by declaring a top node in the UI.</li><br>'
                                        '<li>If you have an empty selection and no top node is declared the checks will run on the entire scene.</li></ol>'
                                        '<p>The documentation will refer to the nodes you are running checks on as your "declared nodes", to not be confused with your active selection.'
                                        '<p>Important! Your current selection will have prioirtiy over the top node defined in the UI. The reason is to be able to quickly debug errror nodes.'
                                        '<p>'
                                        '</p>'
                                        '<b>About</b><p>'    
                                        'modelChecker v' + version + '<p>'
                                        'Reliable production ready sanity checker '
                                        'for Autodesk Maya Sanity check polygon models in Autodesk Maya, '
                                        'and prepare your digital assets for a smooth sailing through '
                                        'the production pipeline. <p>'
                                        'Authors: <ul><li>Jakob Kousholt <li> Niels Peter Kaagaard </ul><p>'
                                        'Contributors: <ul><li>Alberto GZ </ul><p>'
                                        'Contact: jakobjk@gmail.com <p>'
                                        'Website: https://github.com/JakobJK'                                        
                                        )



    def checkCategory(self, category):

        uncheckedCategoryButtons = []
        categoryButtons = []

        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            cat = new[1]
            if cat == category:
                categoryButtons.append(name)
                if self.commandCheckBox[name].isChecked():
                    uncheckedCategoryButtons.append(name)

        for obj in categoryButtons:
            if len(uncheckedCategoryButtons) == len(categoryButtons):
                self.commandCheckBox[obj].setChecked(False)
            else:
                self.commandCheckBox[obj].setChecked(True)


    ## Filter Nodes
    def filterNodes(self):
        nodes = []
        self.SLMesh.clear()
        allUsuableNodes = []
        allNodes = cmds.ls(transforms = True)
        for obj in allNodes:
            if not obj in {'front', 'persp', 'top', 'side'}:
                allUsuableNodes.append(obj)

        selection = cmds.ls(sl = True)
        topNode = self.selectedTopNode_UI.text()
        if len(selection) > 0:
            nodes = selection
        elif self.selectedTopNode_UI.text() == '':
            nodes = allUsuableNodes
        else:
            if cmds.objExists(topNode):
                nodes = cmds.listRelatives(topNode, allDescendents = True, typ='transform')
                if not nodes:
                    nodes = topNode
                nodes.append(topNode)
            else:
                response = 'Object in Top Node doesn`t exists. <font color=#9c4f4f> [ FAILED ] <br>'
                self.reportOutputUI.clear()
                self.reportOutputUI.insertHtml(response)
        for node in nodes:
            shapes = cmds.listRelatives(node, shapes=True, typ='mesh')
            if shapes:
                self.SLMesh.add(node)
        return nodes


    def commandToRun(self, commands):
        cdate = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        # Run FilterNodes
        nodes = self.filterNodes()
        self.reportOutputUI.clear()
        if len(nodes) == 0:
            self.reportOutputUI.insertHtml('No nodes to check. <font color=#9c4f4f> [ FAILED ] <br>')
        else:
            if sceneName != '':
                self.reportOutputUI.insertHtml('Scene: ' + sceneName + '<br>')
            else:
                self.reportOutputUI.insertHtml('Scene: ' + 'Untitled' + '<br>')
            
            self.reportOutputUI.insertHtml('Date: ' + cdate + '<br>')
            self.reportOutputUI.insertHtml('User: ' + username + '<br>')
            self.reportOutputUI.insertHtml('Computer: ' + hostname + '<br>')
            self.reportOutputUI.insertHtml('____________________________<br>')
            
            for command in commands:
                # For Each node in filterNodes, run command.
                self.errorNodes = command(self, nodes)
                self.func_name_fix = ''
                # Return error nodes
                if self.errorNodes:
                    self.reportOutputUI.insertHtml('<br>&#10752; ' + command.func_name + '<font color=#9c4f4f> [ FAILED ] <br>' )
                    for obj in self.errorNodes:
                        self.reportOutputUI.insertHtml('&#9492;&#9472; ' + obj + '<br>')

                    self.errorNodesButton[command.func_name].setEnabled(True)
                    self.errorNodesButton[command.func_name].clicked.connect(partial(self.selectErrorNodes, self.errorNodes))
                    self.commandLabel[command.func_name].setStyleSheet('background-color: #664444;')

                    #Activate FIX button and call to function
                    self.commandFixButton[command.func_name].setEnabled(True)
                    self.commandFixButton[command.func_name].clicked.connect(partial(self.runFix, self.errorNodes, command.func_name, self.func_name_fix ))

                else:
                    self.reportOutputUI.insertHtml('<br> ' + command.func_name + '<font color=#64a65a> [ SUCCESS ] <br>' )
                    self.errorNodesButton[command.func_name].setEnabled(False)
                    self.commandLabel[command.func_name].setStyleSheet('background-color: #446644;')

                    #Deactivate FIX button
                    self.commandFixButton[command.func_name].setEnabled(False)


    # Get info for each check
    def getInfo(self, commands): 
        names = []
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            names.append(name)
                 
        infoList = [ 
                    'trailingNumbers description',  # trailingNumbers
                    'returns any node within the hierachy that is not uniquely named', # duplicatedNames 
                    'returns shape nodes which does not follow the naming convention of transformNode+Shape.', # shapeNames 
                    'returns nodes that are not in the global name space.', # namespaces
        
                    'checks if exists display layers.', # layers
                    'returns any object with construction history.', # history
                    'shaders description', # shaders
                    'returns any object with values for translate and rotate different from 0,0,0 and for scale different from 1,1,1', # unfrozenTransforms
                    'returns any object with pivot values different to world origin (0,0,0).<p>Fix sets to 0,0,0 all pivots.', # uncenteredPivots
                    'parentGeometry description', # parentGeometry
                    'return any exsting empty group. Fix will remove all empty groups.', # emptyGroups
                    'checks if exists user selection sets. Fix will remove all user selection sets.', # selectionSets
                    'returns any object with nodes loaded in Node Editor, that produces MayaNodesInTabs output node.<p>Fix will close all tabs in Node Editor', # nodesInTabs

                    'will return a list of traingles', # triangles
                    'will return a list of polygons with more than 4 points.', # Ngons
                    'will return any edge that is connected to only one face', # openEdges
                    'poles description', # poles
                    'will return any edges that does not have softened normals.', # hardEdges
                    'returns lamina faces.', # lamina
                    'zeroAreaFaces description.', # zeroAreaFaces
                    'returns edges which has a length less than 0.000001 units.', # zeroLengthEdges
                    'noneManifoldEdges description.', # non-manifoldEdges
                    'starlike description.', # starlike 

                    'selfPenetratingUVs description.', # selfPenetratingUVs
                    'returns any polygon object that does have UVs.', # missingUVs
                    'uvRange description.', # uvRange
                    'crossBorder description.' # crossBorder
                    ]
        
        dc = dict(zip(names, infoList))
        
        for command in commands:
            self.reportOutputUI.clear()
            self.reportOutputUI.insertHtml('<br><font color=#c99936>' + command.func_name + '</font> ' + dc[command.func_name] + '<p>' )

        
    # Write the report to report UI.
    def sanityCheck(self):
        self.reportOutputUI.clear()
        checkedCommands = []
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            if self.commandCheckBox[name].isChecked():
                checkedCommands.append(eval(name))
            else:
                self.commandLabel[name].setStyleSheet('background-color: none;')
        if len(checkedCommands) == 0:
            print('You have to select something')
        else:
            self.commandToRun(checkedCommands)

   
    # Write the report to file
    def saveReport(self):
        cdate = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        text = self.reportOutputUI.toPlainText()
        path = scenePath
        reportFile = path + sceneName + '_' + cdate + '.txt'

        if sceneName != '':
            file = codecs.open(reportFile, 'w', 'utf-8')
            file.write(text)
            file.close()
            self.reportOutputUI.insertHtml('<p>____________________________<p>')
            self.reportOutputUI.insertHtml('Report saved! <font color=#3da94d> [ SUCCESS ] </font><br>' + reportFile) 
        else:
            self.reportOutputUI.insertHtml('Save report <font color=#9c4f4f> [ FAILED ] </font><br> You have to save scene before!')
            



    def selectErrorNodes(self, list):
        cmds.select(list)
        '''
        self.reportOutputUI.insertPlainText('selected affected items: \n')
        for i in list:
            self.reportOutputUI.insertPlainText(i + '\n')
        '''


    #this definition needs to run the Fix
    def runFix(self, list, command, func_name_fix):
        nodes = list
        func_name = command
        func_name_fix = command + '_fix'
        globals()[func_name_fix](self, nodes, func_name, func_name_fix)



if __name__ == '__main__':
  try:
      win.close()
  except:
      pass
  win = modelChecker(parent=getMainWindow())
  win.show()
  win.raise_()