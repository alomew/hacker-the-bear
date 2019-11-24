"""
This script demonstrates how to create a bare-bones, fully functional
chatbot using PyAIML.
"""
from __future__ import print_function

import os.path
import sys
import argparse
import io

import aiml

class smarter():


	def __init__(self, mode):

		self.kern = aiml.Kernel()
		self.kern.setTextEncoding( None )

		if mode == "standard":
			chdir = os.path.join( aiml.__path__[0],'botdata','standard' )
			self.kern.bootstrap(learnFiles="startup.xml", commands="load aiml b",
				   chdir=chdir)
		else:
			chdir = os.path.join( aiml.__path__[0],'botdata','alice' )
			self.kern.bootstrap(learnFiles="startup.xml", commands="load alice",
				   chdir=chdir)

	def sendMessage(self, message):
		return self.kern.respond(message)

