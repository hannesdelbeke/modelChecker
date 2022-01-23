<h1 align="center">modelChecker</h1>

modelChecker is a python plug-in written for Autodesk Maya to sanity check digital polygon models. It is unopinionated, provides concise reporting, and lets you select your error nodes easily.

![modelChecker](./modelChecker.png)

## Setup

Download <a href="https://github.com/AlbertoGZ-dev/modelChecker/archive/master.zip">modelChecker.zip</a> and uncompress it.

#### Automatic installation

Run the installer for your plattform.

- Windows by double clicking *install_win.bat* file.
- MacOS by double clicking *install_mac* file.
- Linux open shell and execute *install_linux.sh* file.

Note: on MacOS and Linux you may need to set execution permissions the installer file. Ex. *chmod +x install_linux.sh*

Download the [modelChecker.zip](https://github.com/JakobJK/modelChecker/archive/main.zip) and move the modelChecker folder in your Maya scripts directory and create a python shell button with the following code:

```python
from modelChecker import modelChecker_UI

modelChecker_UI.UI.show_UI()
### add icon to shelf button

For the icon, place *modelChecker_icon.png* file in the same folder as *modelChecker.py*
```

## Usage

There are three ways to run the checks.

1. If you have objects selected the checks will run on the current selection.
2. A hierachy by declaring a top node in the UI.
3. If you have an empty selection and no top node is declared the checks will run on the entire scene.

The documentation will refer to the nodes you are running checks on as your "declared nodes", to not be confused with your active selection.

Important! Your current selection will have prioirtiy over the top node defined in the UI. The reason is to be able to quickly debug errror nodes.

## Checks

Here is an extensive lists of all of the checks the modelChecker can make on your 3d models. Passing all checks does not inherently make for a good model. Understand what is required for your production will.

## Naming

<details>
    <summary>trailingNumbers</summary>
        <p>Returns any node with name ends in any number from 0 to 9.</p>
        <img src="https://github.com/AlbertoGZ-dev/modelChecker/blob/master/website/img/modelChecker_trailingNumbers.png">
</details>

<details>
    <summary>duplicatedNames</summary>
        <p>Returns any node within the hierachy that is not uniquely named</p>
</details>

<details>
    <summary>shapeNames</summary>
        <p>Returns shape nodes which does not follow the naming convention of transformNode+"Shape"</p>
        <img src="https://github.com/AlbertoGZ-dev/modelChecker/blob/master/website/img/modelChecker_shapeNames.png">

</details>

<details>
    <summary>namespaces</summary>
        <p>Returns nodes that are not in the global name space</p>
        <img src="https://github.com/AlbertoGZ-dev/modelChecker/blob/master/website/img/modelChecker_namespaces.png">
</details>

## Topology

<details>
    <summary>triangles</summary>
        <p>Will return a list of traingles</p>
        <img src="https://github.com/AlbertoGZ-dev/modelChecker/blob/master/website/img/modelChecker_triangles.png">
</details>

<details>
    <summary>ngons</summary>
        <p>Will return a list of Ngons</p>
        <img src="https://github.com/AlbertoGZ-dev/modelChecker/blob/master/website/img/modelChecker_ngons.png">
</details>

<details>
    <summary>openEdges</summary>
        <p>Will return any Edge that is connected to onyl one face</p>
        <img src="https://github.com/AlbertoGZ-dev/modelChecker/blob/master/website/img/modelChecker_openEdges.png">
</details>

<details>
    <summary>hardEdges</summary>
        <p>Will return any edges that does not have softened normals</p>
        <img src="https://github.com/AlbertoGZ-dev/modelChecker/blob/master/website/img/modelChecker_hardEdges.png">
</details>

<details>
    <summary>lamina</summary>
        <p>Returns lamina faces</p>
</details>

<details>
    <summary>zeroAreaFaces</summary>
        <p>No description</p>
</details>

<details>
    <summary>zeroLengthEdges</summary>
        <p>Returns edges which has a length less than 0.000001 units</p>
</details>

<details>
    <summary>noneManifoldEdges</summary>
        <p>No description</p>
</details>

<details>
    <summary>starlike</summary>
        <p>No description</p>
</details>

## UVs

<details>
    <summary>selfPenetratingUVs</summary>
        <p>No description</p>
</details>

<details>
    <summary>missingUVs</summary>
        <p>Returns any polygon object that not have UVs</p>
</details>

<details>
    <summary>uvRange</summary>
        <p>No description</p>
</details>

<details>
    <summary>crossBorder</summary>
        <p>No description</p>
</details>

## General

<details>
    <summary>layers </summary>
        <p>Checks if exists display layers</p>
</details>

<details>
    <summary>history</summary>
        <p>Returns any object it have construction history.</p>
</details>

<details>
    <summary>shaders</summary>
        <p>No description</p>
</details>

<details>
    <summary>unfrozenTransforms</summary>
        <p>Returns any object with values for translate and rotate different to 0,0,0 and for scale different to 1,1,1</p>
</details>

<details>
    <summary>uncenteredPivots</summary>
            <p>returns any object with pivot values different to world origin (0,0,0). Fix sets to 0,0,0 all pivots.</p>
</details>

<details>
    <summary>parentGeometry</summary>
        <p>No description</p>
</details>

<details>
    <summary>emptyGroups</summary>
        <p>Return any exsting empty group. Fix will remove all empty groups</p>
</details>

<details>
    <summary>selectionSets</summary>
        <p>Checks if exists user selection sets. Fix will remove all user selection sets.</p>
</details>

<details>
    <summary>nodesInTabs</summary>
        <p>Returns any object with nodes loaded in Node Editor, that produces MayaNodesInTabs output node. Fix will close all tabs in Node Editor</p>
</details>

## Authors

- [**Jakob Kousholt**](https://www.linkedin.com/in/jakobjk/) - Software Engineer / Freelance Creature Modeler
- [**Niels Peter Kaagaard**](https://www.linkedin.com/in/niels-peter-kaagaard-146b8a13) - Senior Modeler at Weta Digital

## Support & Feedback

For any bugs, errors, and requests feel free to reach out to [Jake](mailto:jakobjk@gmail.com)

If you want to support us, feel free to "buy" the modelChecker from [Gumroad](https://jakejk.gumroad.com/l/htZYj).

## License

modelChecker is licensed under the [MIT](https://rem.mit-license.org/) License.
