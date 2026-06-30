# The Anatomic Pathology Lab — An Introduction

An interactive **3D orientation deck** for medical students and transitional-year residents, built for **Dr. Laura Favaza** (Department of Pathology). It walks you through the anatomic-pathology lab **station by station — the journey of a specimen from receipt to sign-out**.

### ▶ View it live
**https://omarzbaba.github.io/ap-lab-orientation/**

Press **▶** to start, then move with the bottom dots / ring / arrow keys / →·Space. Each station reveals one idea at a time, and a real lab photo pops in beside its 3D instrument.

## What's inside
A single self-contained `index.html` (Three.js, vendored locally — runs fully offline) with a stepped "station presenter":

- **The specimen journey:** receipt & accessioning · grossing · fixation · processing · embedding · microtomy · H&E staining · special/IHC · coverslipping · collation · whole-slide scanning · AI assist · pathologist sign-out
- **15 hand-built 3D station dioramas**
- **Real laboratory photographs** that pop in contextually beside each station

## Privacy
All photographs are **de-identified**: patient labels (name, MRN, DOB), accession numbers, and dates have been redacted with opaque boxes. The original un-redacted images and source PowerPoint are **not** part of this repository (excluded via `.gitignore`) and contain PHI. No patient-identifying information is published here.
